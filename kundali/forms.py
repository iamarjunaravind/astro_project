from django import forms

class KundaliForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], widget=forms.Select(attrs={'class': 'form-select'}))
    day = forms.IntegerField(min_value=1, max_value=31, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'DD'}))
    month = forms.IntegerField(min_value=1, max_value=12, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MM'}))
    year = forms.IntegerField(min_value=1900, max_value=2100, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'YYYY'}))
    hour = forms.IntegerField(min_value=0, max_value=23, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'HH (24-hour)'}))
    minute = forms.IntegerField(min_value=0, max_value=59, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MM'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}))
    # State and Country could be added for precision, but keeping it simple for now
