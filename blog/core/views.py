from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Category
from django.db.models import Q


def article_list(request):
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
    
    context = {
        'articles': articles,
        'categories': Category.objects.all(),
    }
    return render(request, 'core/article_list.html', context)

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
    ).exclude(id=article.id).select_related('author').distinct()[:3]
    
    context = {
        'article': article,
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