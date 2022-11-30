from django import forms
from .models import Lab, Profile
 
class LabForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = '__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'