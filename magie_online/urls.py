"""magie_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from magie_online import views

urlpatterns = [
  path('', views.index),
  path('puzzles/', include('puzzles.urls')),
  path('levels/', include('puzzles.levels_urls')),
  path('menus/', include('puzzles.menu_urls')),
  path('admin/', admin.site.urls),
  path('adminapi/categories/', views.get_categories, name='get_categories'),
  path('adminapi/levels/', views.get_levels, name='get_levels'),
  path('adminapi/puzzles/', views.get_puzzles, name='get_puzzles'),
]
