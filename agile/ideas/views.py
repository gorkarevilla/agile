from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.sites.models import Site
from .forms import LoginForm, UserRegistrationForm, EditIdeaForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.template.defaultfilters import striptags, wordwrap
from django.core.mail import EmailMessage
from django.template import RequestContext, Context, loader
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from comments.models import *
from comments.forms import *
from comments.moderator import moderator

from .models import Idea

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

def submit_comment(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
    if comment_form.is_valid():
        cd = form.cleaned_data
	valida = authenticate(comment=cd['comment'], idea_id=cd['idea_id'])

    if valida is not None:            
        comment = comment_form.save(commit=False)          
        messages.add_message(request, messages.SUCCESS, 'You have sucessfully commented!')        
        return HttpResponseRedirect('/ideas/')
        comment.save()
    
    else:
        return render_to_response('ideas/comments.html', {'comment_form': CommentForm,
                'allow_comments':True,
            }, context_instance=RequestContext(request))
         messages.error(request, "You don't have commented")
    else:
return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def edit_idea(request):
	got_id=request.GET.get('id', '')
	user = request.user #TODO: check if user is allowed
	myIdea = Idea.objects.get(id=got_id)
	if request.method == 'POST':
		idea_form = EditIdeaForm(instance=myIdea)
		#idea_form = EditIdeaForm(request.POST)
		if idea_form.is_valid():
			form = idea_form.cleaned_data
			form.save()

		# myIdea.idea_title = cd.title
		# myIdea.idea_text = cd.text

		#myIdea.save()
		return HttpResponseRedirect('/thanks/')  # Redirect after POST
	else:
		form = EditIdeaForm(myIdea)
		print(form)

	return render(request, 'ideas/editIdea.html', {'form': form})



# form = EditIdeaForm(request.POST or None, initial={'idea_title':instance.idea_title, 'idea_text':instance.idea_text})

