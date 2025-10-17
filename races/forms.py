from django import forms


class UploadRaceForm(forms.Form):
    file = forms.FileField()
