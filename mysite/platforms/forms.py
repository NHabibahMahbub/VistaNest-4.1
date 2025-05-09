from django import forms
from .models import Platform, Bid, UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'

    image = forms.ImageField(required=False)


class SearchForm(forms.ModelForm):
    query = forms.CharField(label='Search', max_length=100, required=True)

    class Meta:
        model = Platform
        fields = ['query']


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']


class ComparisonForm(forms.Form):
    properties = forms.ModelMultipleChoiceField(
        queryset=Platform.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Properties for Comparison"
    )


class MarkSoldForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = []


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'about_me', 'photo']


class PasswordChangeFormCustom(PasswordChangeForm):
    pass
