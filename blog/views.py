from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import date
from django.forms import ModelForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from blog.models import Article, Topic, Comment
from blog.forms import ArticleForm, LoginForm

def root(request):
    return HttpResponseRedirect('home')

def home_page(request):
    today = date.today()
    context = {
        'title': 'DJANGO Blog',
        'articles': Article.objects.filter(draft=False).order_by('-published_date')
    }
    response = render(request, 'index.html', context)
    return HttpResponse(response)

def article_page(request, id):
    article = Article.objects.get(pk=id)
    context = {
        'title': 'DJANGO Article',
        'article': article
    }
    response = render(request, 'article_page.html', context)
    return HttpResponse(response)

@require_http_methods(['POST'])
def create_comment(request):
    user_name = request.POST['name']
    user_message = request.POST['message']
    article_id = request.POST['article']
    article = Article.objects.get(id=article_id)
    Comment.objects.create(name=user_name, article=article, message=user_message)
    return redirect('article_page', id=article_id)

# Unable to refactor comment form using ModelForm

@login_required
def create_article(request):
    article_form = ArticleForm()
    return HttpResponse(render(request, 'new_article.html', {'article_form': article_form}))

@login_required
def post_article(request):
    if request.method == 'POST': 
        new_article = ArticleForm(request.POST)
        if new_article.is_valid():
            new = new_article.save(commit=False)
            new.author = request.user
            new.user = request.user
            new_article.save()
            return redirect('article_page', id=new.id)
    else:
        article_form = ArticleForm()
        context = {'article_form': article_form, 'error_msg': 'You have submitted an invalid form, please try again!'}
        response = render(request, 'new_article.html', context)
        return HttpResponse(response)

def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/home')

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            raw_pw = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_pw)
            login(request, user)
            return HttpResponseRedirect('/home')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})