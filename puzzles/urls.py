from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
  path('', views.PuzzlesListView.as_view()),
  path('<pk>', views.PuzzleDetailView.as_view()),
  path('today/', views.DailyPuzzleView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# `static` already configures DEBUG, so no need for this stuff.
# if settings.DEBUG:
#   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
