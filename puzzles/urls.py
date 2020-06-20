from django.urls import path

from . import views

urlpatterns = [
    path('', views.PuzzlesListView.as_view()),
    path('<pk>', views.PuzzleDetailView.as_view()),
]