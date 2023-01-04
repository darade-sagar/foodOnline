from django import forms
from .models import News

class CreateNewsForm(forms.ModelForm):
    short_description = forms.Textarea(attrs={'id':'short_description'})
    long_description = forms.Textarea(attrs={'id':'long_description','class':'form-group'})
    class Meta:
        model = News
        fields = ['title','short_description','long_description']