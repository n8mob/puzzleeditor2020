
from django import forms

class CharCounterTextInput(forms.widgets.TextInput):
	
	def render(self, name, value, attrs=None, renderer=None):
		attrs.update({'class': 'char-counter-text-input'})
		ret_html = super(CharCounterTextInput, self).render(name, value, attrs, renderer)
		if not value:
			value = ''

		return ('{}<div class="counter"><span class="input-counter">{}</span> chars</div>').format(ret_html, len(value))