from django import forms
from .models import AirportRoute


class AddRouteForm(forms.ModelForm):
    class Meta:
        model = AirportRoute
        fields = ['airport_code', 'position', 'duration']
        widgets = {
            'airport_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. JFK'}),
            'position': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class NthSearchForm(forms.Form):
    airport_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direction = forms.ChoiceField(choices=(('left', 'Left'), ('right', 'Right')), widget=forms.Select(attrs={'class': 'form-select'}))
    n = forms.IntegerField(min_value=1, label='N (1-based)', widget=forms.NumberInput(attrs={'class': 'form-control'}))


class BetweenAirportsForm(forms.Form):
    airport_code_a = forms.CharField(max_length=10, label='Airport A', widget=forms.TextInput(attrs={'class': 'form-control'}))
    airport_code_b = forms.CharField(max_length=10, label='Airport B', widget=forms.TextInput(attrs={'class': 'form-control'}))
