from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),
    path('news/add/', views.add_news_view, name='add_news'),
    path('news/<int:news_id>/edit/', views.edit_news_view, name='edit_news'),
    path('news/<int:news_id>/delete/', views.delete_news_view, name='delete_news'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/delete/', views.delete_profile_view, name='delete_profile'),
]