import json
import uuid
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.http import HttpResponse, JsonResponse

from puzzles.models import Category, Level, Puzzle


def index(request):
  host = request.get_host()
  uuid_for_host = str(uuid.uuid5(uuid.NAMESPACE_DNS, host))
  timestamp = datetime.now()

  response = {
    'my_uuid': uuid_for_host,
    'timestamp': timestamp,
  }

  return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))


@staff_member_required
def get_categories(request):
  menu_id = request.GET.get('menu_id')
  categories = []
  if menu_id:
    categories = list(Category.objects.filter(menu_id=menu_id).values('id', 'name'))
  return JsonResponse(categories, safe=False)


@staff_member_required
def get_levels(request):
  category_id = request.GET.get('category_id')
  levels = []
  if category_id:
    level_objects = Level.objects.filter(category_id=category_id)

    levels = [{
      'levelNumber': level.levelNumber,
      'sort_order': level.sort_order,
      'display_name': str(level)
    } for level in level_objects]
    levels = sorted(levels, key=lambda x: x['sort_order'])
  return JsonResponse(levels, safe=False)


@staff_member_required
def get_puzzles(request):
  level_id = request.GET.get('level_id')
  puzzles = []
  if level_id:
    puzzles = list(Puzzle.objects.filter(level_id=level_id).values('id', 'name'))
  return JsonResponse(puzzles, safe=False)
