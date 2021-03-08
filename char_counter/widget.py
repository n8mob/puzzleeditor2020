
from django import forms

class CharCounterTextInput(forms.widgets.TextInput):
	
	def render(self, name, value, attrs=None, renderer=None):
		attrs.update({'class': 'char-counter-text-input'})

		textinput_html = super(CharCounterTextInput, self).render(name, value, attrs, renderer)

		if not value:
			value = ''

		charcounter_html = f'<div class="counter"><span class="input-counter">{len(value)}</span> chars</div>'

		return (f"{textinput_html}{charcounter_html}")
