from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone

from .models import Article, Category, ArticleView
from .utils import get_user_ip_address


def home(request):
    """Display list of published articles with pagination"""

    # Get latest articles (excluding featured ones for main grid)
    articles_list = Article.objects.filter(
        published=True
    ).select_related('author').prefetch_related('categories').order_by('-created_at')
    
    # Pagination - 9 articles per page
    paginator = Paginator(articles_list, 9)
    page = request.GET.get('page')
    
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    
    # Get popular articles
    from django.db.models import Count
    popular_articles = Article.objects.filter(published=True).annotate(
        view_count=Count('articleview')
    ).order_by('-view_count')[:4]


    
    context = {
        'articles': articles,
        'categories': Category.objects.all(),
        'popular_articles': popular_articles,
    }
    return render(request, 'core/home.html', context)

def article_detail(request, slug):
    """Display single article detail with optimized queries"""
    article = get_object_or_404(
        Article.objects.select_related('author').prefetch_related('categories'),
        slug=slug, 
        published=True
    )
    
    # Get related articles (same category)
    related_articles = Article.objects.filter(
        categories__in=article.categories.all(),
        published=True
    ).exclude(id=article.id).select_related('author').distinct()[:20]

    user_ip = get_user_ip_address(request)
    today = timezone.now().date()

    # Track view (unique per user_ip per article)
    ArticleView.objects.get_or_create(
        article=article,
        user_ip=user_ip,
        created_at__date=today
    )

    article_views = ArticleView.objects.filter(article=article).count()

    context = {
        'article': article,
        'article_views': article_views,
        'related_articles': related_articles,
        'categories': Category.objects.all()
    }
    return render(request, 'core/article_detail.html', context)

def articles_by_category(request, slug):
    """Display articles filtered by category with optimized queries"""
    category = get_object_or_404(Category, slug=slug)
    articles_list = Article.objects.filter(
        categories=category, 
        published=True
    ).select_related('author').prefetch_related('categories').order_by('-created_at')
    
    paginator = Paginator(articles_list, 6)
    page = request.GET.get('page')
    
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    
    context = {
        'articles': articles,
        'category': category,
        'categories': categories,
    }
    return render(request, 'core/articles_by_category.html', context)


def search_articles(request):
    """Search functionality for articles"""
    query = request.GET.get('q')
    articles = Article.objects.filter(published=True)
    
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct().order_by('-created_at')
    
    categories = Category.objects.all()
    
    context = {
        'articles': articles,
        'query': query,
        'categories': categories,
    }
    return render(request, 'core/search_results.html', context)


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import NewsletterForm

@require_POST
def subscribe(request):
    data = request.POST
    form = NewsletterForm(data)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing!'})
    else:
        # Check if email is invalid or already exists
        if 'email' in form.errors:
            error_msg = form.errors['email'][0]
            if "already exists" in error_msg:
                 return JsonResponse({'status': 'error', 'message': 'This email is already subscribed.'}, status=400)
            return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)