from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import date
from django.forms import ModelForm
from django.views.decorators.http import require_http_methods
from blog.models import Article, Topic, Comment
from blog.forms import ArticleForm

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

def create_article(request):
    article_form = ArticleForm()
    return HttpResponse(render(request, 'new_article.html', {'article_form': article_form}))

def post_article(request):
    new_article = ArticleForm(request.POST)
    if new_article.is_valid():
        new_article.save()
        new_article.id = id
        return HttpResponseRedirect('/home')
    else:
        article_form = ArticleForm()
        context = {'article_form': article_form, 'error_msg': 'You have submitted an invalid form, please try again!'}
        response = render(request, 'new_article.html', context)
        return HttpResponse(response)