from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Lab, Profile
 
class LabForm(forms.ModelForm):
    """
    The Lab Form
    """
    class Meta:
        model = Lab
        fields = '__all__'


class ExtendedUserCreationForm(UserCreationForm):
    """
    The User Creation Form
    """
    email=forms.EmailField(required=True)
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']

        if commit :
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    """
    The User Profile Form
    """
    class Meta:
        model = Profile
        fields = ('comorbidity', 'race', 'gender', 'phone', 'weight', 'height', 'birth_date')
