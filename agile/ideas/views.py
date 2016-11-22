from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.views.decorators.http import require_http_methods

from ideas.forms import CommentForm, IdeaForm, EditIdeaForm

from .forms import LoginForm, UserRegistrationForm
from .models import Idea


# Create your views here.
@require_http_methods(["GET"])
def index(request):
	return render (request, 'ideas/index.html')

@require_http_methods(["GET"])
def main(request):
	return render (request, 'ideas/main.html')

def show_idea(request): 
	id= request.GET.get('id','')
	idea = Idea.objects.get(pk=id)
	return render(request, 'ideas/detail.html', {'idea':idea})

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

@login_required
@require_http_methods(["GET"])
def user_logout(request): 
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'You have successfully loged out!')
	return HttpResponseRedirect('/ideas/')
	
@login_required()
def submit_comment (request):
	if request.method == 'POST':
			comment_form = CommentForm(request.POST)
			
			if comment_form.is_valid():
				cd = comment_form.cleaned_data
				valida = authenticate(comment=cd['comment'], idea_id=cd['idea_id'])
				
				if valida is not None:
					comment = comment_form.save(commit=False)
					messages.add_message(request, messages.SUCCESS, 'You have successfully commented!')
					return HttpResponseRedirect('/ideas/')
					comment.save()
				else:
					return render_to_response('ideas/comments.html', {'comment_form': CommentForm,'allow_comments':True,}, context_instance=RequestContext(request))
					messages.error(request, 'You don\'t have commented')
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFER', '/'))

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
			ideat = idea_form.cleaned_data['idea_text']
			if Idea.objects.filter(idea_title=title).count() == 0:
				idea = idea_form.save(commit=False)
				idea.idea_title = title
				idea.idea_text = ideat
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

@login_required()
def edit_idea(request):
	if request.method == 'GET':
		id=request.GET.get('id', '')
		my_idea = Idea.objects.get(pk=id)
		user = request.user
		if (my_idea.creator == user):
			form = EditIdeaForm(initial={'idea_title':my_idea.idea_title, 'idea_text':my_idea.idea_text})
			return render(request, 'ideas/editIdea.html', {'form':form})
		else: 
			messages.add_message(request, messages.ERROR, 'You can only modify your idea')
			return HttpResponseRedirect('/ideas/')
	elif request.method == 'POST':
		form = EditIdeaForm(request.POST)
		if form.is_valid(): 
			cd = form.cleaned_data
			old_idea = Idea.objects.get(pk=1)
			if (old_idea is not None) and (len(old_idea) > 0): 
				old_idea.update(idea_title=cd['idea_title'])
				messages.success(request,"Iddea modified")
				return HttpResponseRedirect('/ideas')
			else: 
				messages.error(request, "There was an error while editing the idea")
				return HttpResponseRedirect('/ideas')
		else: 
			messages.error(request, "Form invalid")
			return HttpResponseRedirect('/ideas')




# form = EditIdeaForm(request.POST or None, initial={'idea_title':instance.idea_title, 'idea_text':instance.idea_text})
