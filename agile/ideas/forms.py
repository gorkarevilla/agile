# -*- coding: utf-8 -*-

from django import forms 
from django.contrib.auth.models import User

from ideas.models import Idea

from .models import Comment


class LoginForm(forms.Form): 
	username = forms.CharField(label='User')
	password = forms.CharField(label='Password',widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm): 
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password_2 = forms.CharField(label='Please repeat password', widget=forms.PasswordInput)

	class Meta: 
		model = User
		fields = ('username','first_name','last_name','email',)
	
	def check_password(self): 
		cd = self.cleaned_data
		if cd['password'] != cd['password_2']: 
			raise forms.ValidationError('Passwords do not match')
		return cd['password_2']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment', 'idea_id', 'user_name')
		widgets = {'idea_id': forms.HiddenInput(), 'user_name': forms.HiddenInput()}
		
class IdeaForm(forms.ModelForm):
	idea_title = forms.CharField(label='Idea title', widget=forms.TextInput(attrs={'placeholder':'Length 3-50 char.'}))
	idea_text = forms.CharField(label='Idea text', widget=forms.Textarea)
	class Meta:
		model = Idea
		fields = ('idea_title', 'idea_text')

class EditIdeaForm(forms.Form):
	idea_title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder':'Length 3-50 char.'}))
	idea_text = forms.CharField(label='Text', widget=forms.Textarea)
	
	class Meta:
		model = Idea
		widgets = {'idea_id': forms.HiddenInput()}
		
class FilterIdeasForm(forms.Form):
	keywordfilter_text = forms.CharField(label='Search by Title', max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder':'No filter applied'}))