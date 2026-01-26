from django import forms
from .models import Service
from .models import Review

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['provider', 'created_at', 'updated_at']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']