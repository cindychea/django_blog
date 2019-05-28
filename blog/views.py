from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import date
from django.views.decorators.http import require_http_methods
from blog.models import Article, Topic, Comment

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