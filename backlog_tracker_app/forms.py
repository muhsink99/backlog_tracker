from django import forms 
from django.core import validators
from django.contrib.auth.models import User
from backlog_tracker_app.models import UserProfile

class UserForm(forms.ModelForm): 
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',

        }
    )) 
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    verify_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta(): 
        model = User 
        fields = ('username', 'email', 'verify_email', 'password')

    def clean(self): 
        all_clean_data = super().clean() 

        email = all_clean_data['email']
        v_email = all_clean_data['verify_email']

        if (email != v_email): 
            raise forms.ValidationError(('Your e-mails do not match.'), code='invalid')

class UserProfileForm(forms.ModelForm): 
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta(): 
        model = UserProfile
        fields = ('profile_pic',)