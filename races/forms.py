from django import forms


class UploadRaceForm(forms.Form):
    title = forms.CharField(max_length=256)
    file = forms.FileField()
