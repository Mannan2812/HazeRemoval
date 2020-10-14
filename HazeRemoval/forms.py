from django import forms
class ImageUploadForm(forms.Form):
    img = forms.ImageField()