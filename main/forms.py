
# forms.py
from django import forms
from .models import *
  
class ImageForm(forms.ModelForm):
  
    class Meta:
        model = Directory
        fields = ['directory_name', 'image_path']
        labels = {
        "directory_name": "Name",
        "image_path" : "Choose Image"
    }
