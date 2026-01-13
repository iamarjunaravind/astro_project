from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class AstrologerRegistrationForm(UserRegistrationForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    experience_years = forms.IntegerField(min_value=0, required=True)

    class Meta(UserRegistrationForm.Meta):
        fields = UserRegistrationForm.Meta.fields + ['bio', 'experience_years']

from astromall.models import Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']
