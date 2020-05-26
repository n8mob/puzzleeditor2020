from rest_framework import generics

from puzzles.models import Puzzle
from puzzles.serializers import PuzzleSerializer


class PuzzlesListView(generics.ListCreateAPIView):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer


class PuzzleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer
