from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from .models import News
from .forms import NewsForm, UserRegisterForm, UserUpdateForm

def home_view(request):
    news_list = News.objects.all().order_by('-date_created')
    paginator = Paginator(news_list, 5)  # 5 новостей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})

def news_detail_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    is_author = news.author == request.user if request.user.is_authenticated else False
    return render(request, 'news_detail.html', {'news': news, 'is_author': is_author})

@login_required
def add_news_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость успешно добавлена!')
            return redirect('home')
    else:
        form = NewsForm()
    return render(request, 'news_form.html', {'form': form, 'title': 'Добавить новость'})

@login_required
def edit_news_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать эту новость")
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно обновлена!')
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news_form.html', {'form': form, 'title': 'Редактировать новость'})

@login_required
def delete_news_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить эту новость")
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость успешно удалена!')
        return redirect('home')
    return render(request, 'news_confirm_delete.html', {'news': news})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вход выполнен!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Аккаунт удален.')
        return redirect('home')
    return render(request, 'profile_delete.html')
