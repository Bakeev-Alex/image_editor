from .models import ImageArticle
from django import forms

class ImageArticleForm(forms.ModelForm):
    class Meta:
        model = ImageArticle
        fields = ['picture_name']