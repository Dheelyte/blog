from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_articles, name='search_articles'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('cookies/', views.cookies, name='cookies'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('category/<slug:slug>/', views.articles_by_category, name='articles_by_category'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]
