from django import forms
from .models import Selfie

class SelfieForm(forms.ModelForm):
    class Meta:
        model = Selfie
        fields = ['store', 'image', 'review']