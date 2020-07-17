from django import forms
from chores.models import Chore, ChoreInterval


class ChoreForm(forms.ModelForm):

    class Meta:
        model = Chore
        fields = ('name', 'description', 'repeats')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'description': forms.Textarea(),
            'repeats': forms.CheckboxInput(attrs={'class': 'chore-repeats', 'id': 'choreRepeatsCheckbox'}),
        }


class ChoreIntervalForm(forms.ModelForm):

    class Meta:
        model = ChoreInterval
        fields = ('repeat_start', 'repeat_interval', 'repeat_custom_interval')

        widgets = {
            'repeat_start': forms.DateTimeInput(),
            'repeat_interval': forms.RadioSelect(),
            'repeat_custom_interval': forms.NumberInput(),
        }
