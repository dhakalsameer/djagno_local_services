# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    city = forms.CharField(max_length=50, required=True)
    profile_photo = forms.ImageField(required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'city', 'profile_photo']

    def save(self, commit=True):
        # Save the User object
        user = super().save(commit)
        role = self.cleaned_data['role']
        city = self.cleaned_data['city']
        profile_photo = self.cleaned_data.get('profile_photo')

        # Create the Profile object
        Profile.objects.create(
            user=user,
            role=role,
            city=city,
            profile_photo=profile_photo
        )
        return user
