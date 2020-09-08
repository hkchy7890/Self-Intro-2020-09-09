from django import forms
from .models import Enquiry, Post

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        labels = {
            'content':'Comment'
        }
        fields = '__all__'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']
