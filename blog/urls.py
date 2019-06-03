"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from blog.views import *
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('', root),
    path('home/', home_page, name='home'),
    path('admin/', admin.site.urls),
    path('article/<int:id>', article_page, name='article_page'),
    path('article/<int:id>/edit', edit_article, name='edit_article'),
    path('article/create', create_article, name='create_article'),
    path('article/post', post_article, name='post_article'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    path('signup/', signup, name='signup'),
    path('article/<int:id>/comment', post_comment, name='post_comment')
]
