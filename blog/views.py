from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import date

def root(request):
    return HttpResponseRedirect('home')

def home_page(request):
    today = date.today()
    context = {
        'current_date': today,
        'status_code_link': 'https://httpstatuses.com/',
    }
    response = render(request, 'index.html', context)
    return HttpResponse(response)