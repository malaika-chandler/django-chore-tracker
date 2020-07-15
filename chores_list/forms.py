from django import forms
from django.utils import timezone
from chores_list.models import Chore, ChoreInterval


class ChoreForm(forms.ModelForm):

    class Meta:
        model = Chore
        fields = ('name', 'description', 'repeats')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'description': forms.Textarea(),
            'repeats': forms.CheckboxInput(),
        }


class ChoreIntervalForm(forms.ModelForm):

    class Meta:
        model = ChoreInterval
        fields = ('repeat_interval', 'repeat_day_of_year')

        widgets = {
            'repeat_interval': forms.DateTimeInput(),
            'repeat_day_of_the_year': forms.NumberInput(),
        }
