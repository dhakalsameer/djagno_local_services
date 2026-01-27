from django import forms
from .models import Service, ServiceCategory
from .models import Review , Profile


class ServiceForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100,
        required=False,
        label="Or Add New Category",
        widget=forms.TextInput(attrs={'placeholder': 'Add new category...'})
    )

    class Meta:
        model = Service
        fields = ['category', 'title', 'description', 'price', 'price_type', 'location', 'is_active']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # <- handle user here
        super().__init__(*args, **kwargs)
        # Sort categories alphabetically
        self.fields['category'].queryset = ServiceCategory.objects.all().order_by('name')




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'city', 'profile_photo']