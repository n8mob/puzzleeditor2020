from django import forms

from puzzles.models import Category, DailyPuzzle, Level, Menu, Puzzle


class DailyPuzzleForm(forms.ModelForm):
  menu = forms.ModelChoiceField(queryset=Menu.objects.all(), required=False)
  category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)
  level = forms.ModelChoiceField(queryset=Level.objects.none(), required=False)

  class Meta:
    model = DailyPuzzle
    fields = ['date', 'menu', 'category', 'level', 'puzzle']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if 'menu' in self.data:
      try:
        menu_id = int(self.data.get('menu'))
        self.fields['category'].queryset = Category.objects.filter(menu_id=menu_id).order_by('name')
      except (ValueError, TypeError):
        pass
    if 'category' in self.data:
      try:
        category_id = int(self.data.get('category'))
        self.fields['level'].queryset = Level.objects.filter(category_id=category_id).order_by('sort_order')
      except (ValueError, TypeError):
        pass
    if 'level' in self.data:
      try:
        level_id = int(self.data.get('level'))
        self.fields['puzzle'].queryset = Puzzle.objects.filter(level_id=level_id).order_by('puzzle_number')
      except (ValueError, TypeError):
        pass
    else:
      self.fields['puzzle'].queryset = Puzzle.objects.none()
