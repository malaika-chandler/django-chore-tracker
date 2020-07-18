from django import forms
from django.utils import safestring
from chores.models import Chore, ChoreInterval


class ChoreForm(forms.ModelForm):

    class Meta:
        model = Chore
        fields = ('name', 'description', 'datetime', 'repeats')
        labels = {
            'datetime': safestring.mark_safe('<span class="glyphicon glyphicon-time"></span>'),
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'description': forms.Textarea(),
            'datetime': forms.DateTimeInput(attrs={'placeholder': 'Enter a date and time'}),
            'repeats': forms.CheckboxInput(attrs={'class': 'chore-repeats', 'id': 'choreRepeatsCheckbox'}),
        }


class ChoreIntervalForm(forms.ModelForm):

    class Meta:
        model = ChoreInterval
        fields = ('repeat_interval', 'repeat_custom_interval')

        widgets = {
            'repeat_interval': forms.RadioSelect(),
            'repeat_custom_interval': forms.NumberInput(),
        }
