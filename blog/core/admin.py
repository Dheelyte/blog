from django.contrib import admin
from .models import Article, Category
from django import forms
from ckeditor.widgets import CKEditorWidget


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            # Add CKEditor widget for content field
            'content': CKEditorWidget(),
        }

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'categories', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'tags__name', 'categories__name')
    filter_horizontal = ('categories',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'thumbnail')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Categorization', {
            'fields': ('categories',)
        }),
        ('Publication', {
            'fields': ('published',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
        
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('categories')
    
    actions = ['make_published', 'make_unpublished']
    
    def make_published(self, request, queryset):
        updated = queryset.update(published=True)
        self.message_user(request, f'{updated} articles were successfully published.')
    make_published.short_description = "Mark selected articles as published"
    
    def make_unpublished(self, request, queryset):
        updated = queryset.update(published=False)
        self.message_user(request, f'{updated} articles were successfully unpublished.')
    make_unpublished.short_description = "Mark selected articles as unpublished"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'article_count')
    search_fields = ('name',)
    
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Number of Articles'


# Register models
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
