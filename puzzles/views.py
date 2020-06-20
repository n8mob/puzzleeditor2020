from rest_framework import generics

from puzzles.models import Puzzle, Level
from puzzles.serializers import PuzzleSerializer, LevelSerializer


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
