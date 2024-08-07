import datetime
import zoneinfo

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
