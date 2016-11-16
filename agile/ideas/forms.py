from django import forms
from django.contrib.auth.models import User
from .models import Comment

# Comment Ideas Form


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'idea_id')
        widgets = {'idea_id': forms.HiddenInput()}
