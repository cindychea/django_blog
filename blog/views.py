from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import date
from blog.models import Article, Topic

def root(request):
    return HttpResponseRedirect('home')

def home_page(request):
    today = date.today()
    context = {
        'current_date': today,
        'articles': Article.objects.filter(draft=False).order_by('-published_date')
    }
    response = render(request, 'index.html', context)
    return HttpResponse(response)