from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_articles, name='search_articles'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.articles_by_category, name='articles_by_category'),
]