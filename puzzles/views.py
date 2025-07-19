import datetime
import time
import zoneinfo

from django.utils.http import http_date
from django.views.decorators.http import last_modified
from rest_framework import generics
from rest_framework.response import Response

from puzzles.models import DailyPuzzle, Level, Menu, Puzzle
from puzzles.serializers import DailyPuzzleSerializer, LevelSerializer, MenuSerializer, PuzzleSerializer


class MenuListView(generics.ListCreateAPIView):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer


class MenuDetailView(generics.RetrieveAPIView):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer
  lookup_field = 'name'

  def get(self, request, *args, **kwargs):
    instance: Menu = self.get_object()
    updated_at = instance.updated_at.timestamp()
    updated_at_http = http_date(updated_at)

    if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE')
    if if_modified_since:
      try:
        since_ts = time.mktime(time.strptime(if_modified_since, "%a, %d %b %Y %H:%M:%S %Z"))
        if int(since_ts) >= int(updated_at):
          return Response(status=304)
      except Exception:
        # ignore
        pass

    serializer = self.get_serializer(instance)
    response = Response(serializer.data)
    response.headers['Last-Modified'] = updated_at_http
    return response


class LevelsListView(generics.ListCreateAPIView):
  queryset = Level.objects.all()
  serializer_class = LevelSerializer


class LevelDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Level.objects.all()
  serializer_class = LevelSerializer


class PuzzlesListView(generics.ListCreateAPIView):
  queryset = Puzzle.objects.all()
  serializer_class = PuzzleSerializer


class PuzzleDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Puzzle.objects.all()
  serializer_class = PuzzleSerializer


class DailyPuzzleView(generics.RetrieveAPIView):
  queryset = Puzzle.objects.all()
  serializer_class = DailyPuzzleSerializer
  lookup_field = 'date'

  def get(self, request, *args, **kwargs):
    local_zone = zoneinfo.ZoneInfo('America/Denver')
    local_now = datetime.datetime.now(local_zone)
    today = DailyPuzzle.objects.filter(date=local_now.date()).first()

    serializer = self.get_serializer(today)
    return Response(serializer.data)


class DailyPuzzleTest(generics.RetrieveAPIView):
  queryset = DailyPuzzle.objects.all()
  serializer_class = DailyPuzzleSerializer
  lookup_field = 'date'

  def get(self, request, *args, **kwargs):
    year = int(kwargs.get('year'))
    month = int(kwargs.get('month'))
    day = int(kwargs.get('day'))

    # Use the extracted parameters as needed
    test_date = datetime.date(year, month, day)
    date_puzzle = DailyPuzzle.objects.filter(date=test_date).first()
    if date_puzzle is None:
      return Response({'error': 'No puzzle found for this date'}, status=404)

    serializer = self.get_serializer(date_puzzle)
    return Response(serializer.data)
