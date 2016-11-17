from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ideas.forms import IdeaForm
from models import Idea

from .forms import LoginForm, UserRegistrationForm
from django.template.defaultfilters import title


# Create your views here.
@require_http_methods(["GET"])
def index(request):
	return render (request, 'ideas/index.html')

def user_login(request):
	if request.method == 'GET': 
		form = LoginForm()
		return render (request, 'ideas/login.html', {'form':form})
	if request.method == 'POST': 
		form = LoginForm(request.POST)

		if form.is_valid(): 
			cd = form.cleaned_data
			user = authenticate(username=cd['username'], password=cd['password'])
			
			if user is not None: 
				login(request,user)
				messages.add_message(request, messages.SUCCESS, 'You have sucessfully logged in!')
				return HttpResponseRedirect('/ideas/')
			else:
				messages.error(request, "Wrong user or password")
				return render(request, 'ideas/login.html', {'form':LoginForm})
		else: 
			messages.error(request, "Wrong user or password")
			return render(request, 'ideas/login.html', {'form':LoginForm})
	else: 
		return HttpResponse("I'm lost")

def user_signup(request): 
	if request.method == 'POST': 
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid(): 
			new_user = user_form.save(commit=False)
			new_user.set_password(
				user_form.cleaned_data['password'])
			new_user.save()
			messages.add_message(request, messages.SUCCESS, 'User successfully created!')
			return HttpResponseRedirect('/ideas/')
	else: 
		user_form = UserRegistrationForm()
	return render(request,'ideas/signup.html', {'user_form':user_form})

def add_idea (request):
	if request.method == 'GET':
		form = IdeaForm()
		return render (request, 'ideas/addIdea.html', {'form':form})
	if request.method == 'POST':
		idea_form = IdeaForm(request.POST)
		
		if idea_form.is_valid():
			title = idea_form.cleaned_data['idea_title']
			idea = idea_form.cleaned_data['idea_text']
			if Idea.objects.filter(idea_title=title).count() == 0:
				idea = idea_form.save(commit=False)
				idea.idea_title = title
				idea.idea_text = idea
				idea.creator = request.user
				idea.save()
				messages.add_message(request, messages.SUCCESS, 'You have sucessfully created an idea!')
	
				return HttpResponseRedirect('/ideas/')
			else:
				messages.add_message(request, messages.ERROR, 'Idea with same title already created!')
				return HttpResponseRedirect('/ideas/')
		else:
			messages.add_message(request, messages.ERROR, 'ERROR EN EL FORULARIO!')
			return HttpResponseRedirect('/ideas/')
		
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		