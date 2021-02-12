from django.urls import path

from . import views

urlpatterns = [
    path('', views.MenuListView.as_view()),
    path('<name>', views.MenuDetailView.as_view()),
]
