# -*- coding: utf-8 -*-

from django import forms 
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Field, Submit
from crispy_forms.bootstrap import InlineCheckboxes, FormActions, StrictButton

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


class EditIdeaForm(forms.Form):
   idea_title = forms.CharField(label='Title')
   idea_text = forms.CharField(label='Text')
