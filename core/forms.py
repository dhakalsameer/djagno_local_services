from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['provider', 'created_at', 'updated_at']
