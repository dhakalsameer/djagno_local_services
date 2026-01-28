from django import forms
from django.contrib.auth.models import User
from core.models import Profile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    profile_photo = forms.ImageField(required=False)  # add profile photo field

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        # Create the User instance
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            # Create Profile linked to the user
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                profile_photo=self.cleaned_data.get('profile_photo')
            )

        return user
