import datetime
import logging
import zoneinfo

from rest_framework import generics
from rest_framework.response import Response

from puzzles.models import Level, Menu, Puzzle
from puzzles.serializers import LevelSerializer, MenuSerializer, PuzzleSerializer


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
  serializer_class = PuzzleSerializer
  lookup_field = 'puzzle_number'

  def get(self, request, *args, **kwargs):
    local_zone = zoneinfo.ZoneInfo('America/Denver')
    local_now = datetime.datetime.now(local_zone)
    random_puzzle = Puzzle.objects.order_by('?').first()

    serializer = self.get_serializer(random_puzzle)
    return Response(serializer.data)
