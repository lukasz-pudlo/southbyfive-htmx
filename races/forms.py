from django import forms
from django.forms import ModelForm
from .models import RaceFile


class UploadRaceForm(forms.ModelForm):
    class Meta:
        model = RaceFile
        fields = '__all__'
