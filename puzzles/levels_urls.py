from django.urls import path

from . import views

urlpatterns = [
    path('', views.LevelsListView.as_view()),
    path('<pk>', views.LevelDetailView.as_view()),
]