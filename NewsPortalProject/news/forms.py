from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from .models import Post, Author

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'heading',
            'text',
            'categories',
        ]


