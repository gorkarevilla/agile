from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.views.decorators.http import require_http_methods

from ideas.forms import CommentForm, IdeaForm, EditIdeaForm, FilterIdeasForm
from ideas.models import Comment

from .forms import LoginForm, UserRegistrationForm
from .models import Idea


# Create your views here.
@require_http_methods(["GET"])
def index(request):
	return render (request, 'ideas/index.html')

#@require_http_methods(["GET"])
#def main(request):
#	return render (request, 'ideas/main.html')

@login_required()
def idea_list(request):
	filterlistideas_form = FilterIdeasForm(request.POST or None)
	ideas=Idea.objects.all()
		
	filter = request.POST.get('keywordfilter_text',False)

	if request.method == 'GET' and 'delete' in request.GET:
		deleteid = request.GET['delete']
		if deleteid is not None and deleteid !='':
			idea = Idea.objects.get(pk = deleteid)
			if request.user == idea.creator:
				idea.delete()
				messages.success(request,"Idea deleted")
			else:
				messages.error(request,"You can not delete the idea. You are not the owner.") 

	if request.method == 'GET':
				
		return render(request, 'ideas/main.html', {'ideas':ideas, 'filterform':filterlistideas_form})
	
	if request.method == 'POST':

		if filterlistideas_form.is_valid():
			if filter=='':
				ideas=Idea.objects.all()
			else:
				ideas=Idea.objects.all().filter(idea_title__icontains=filter)		
		
		return render(request, 'ideas/main.html', {'ideas':ideas, 'filterform':filterlistideas_form})

def show_idea(request):
	if request.method == 'GET':
		idea1= request.GET.get('id', '')
		idea = Idea.objects.get(id=idea1)
		comments =Comment.objects.filter(idea_id=idea)
		return render(request, 'ideas/detail.html', {'idea':idea, 'comments':comments})

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
	
@login_required(login_url="/ideas/login")
def submit_comment (request):
	if request.method == 'GET':
		id = request.GET.get('id')		
		form = CommentForm(initial={'idea_id':id, 'user_name':request.user})
		return render (request, 'ideas/comment.html' , {'form':form})
	if request.method == 'POST':		
		comment_form = CommentForm(request.POST)
	
		if comment_form.is_valid():
			cd = comment_form.cleaned_data
			comment = comment_form.save(commit=False)
			comment.save()
			messages.add_message(request, messages.SUCCESS, 'You have successfully commented!')
			return HttpResponseRedirect('/ideas/')
		else:
			messages.error(request, 'Your comment could not be added, it was not valid!')
			return HttpResponseRedirect('/ideas/')


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

@login_required(login_url="/ideas/login")
def edit_idea(request):
	if request.method == 'GET':
		id=request.GET.get('id', '')
		my_idea = Idea.objects.get(pk=id)
		user = request.user
		if (my_idea.creator == user) or (request.user.is_superuser):
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
			if (old_idea is not None): 
				old_idea.idea_title=cd['idea_title']
				old_idea.idea_text=cd['idea_text']
				old_idea.save()
				messages.success(request,"Idea modified")
				return HttpResponseRedirect('/ideas')
			else: 
				messages.error(request, "There was an error while editing the idea")
				return HttpResponseRedirect('/ideas')
		else: 
			messages.error(request, "Form invalid")
			return HttpResponseRedirect('/ideas')




# form = EditIdeaForm(request.POST or None, initial={'idea_title':instance.idea_title, 'idea_text':instance.idea_text})

@login_required
def deleteComment(request):
	if request.method == 'GET':
		id = request.GET.get('id')	
		my_comment = Idea.objects.get(pk=id)
		#user = request.user	
		if (request.user.is_superuser):
			#form = CommentForm(initial={'idea_id':id, 'user_name':request.user})
			form = CommentForm(initial={'comment':my_comment.comment})	
			return render(request, 'ideas/deleteComment.html', {'form':form})
		else: 
			messages.add_message(request, messages.ERROR, 'You can not delete the comment. You are not the superuser')
			return HttpResponseRedirect('/ideas/')	
	if request.method == 'POST':			 		
		form = CommentForm(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			comment = form.delete(commit=False)			
			#comment_form = Idea.objects.get(pk=1)	
			#if (comment_form is not None):
			#comment_form.comment=cd['comment']			
			comment.delete()
			messages.add_message(request, "You have deleted the comment")
			return HttpResponseRedirect('/ideas/')
		else:
			messages.error(request, 'you can not delete')
			return HttpResponseRedirect('/ideas/')


@login_required()
def deleteIdea(request):
	filterlistideas_form = FilterIdeasForm(request.POST or None)
	ideas=Idea.objects.all()
		
	filter = request.POST.get('keywordfilter_text',False)

	if request.method == 'GET' and 'delete' in request.GET:
		deleteid = request.GET['delete']
		if deleteid is not None and deleteid !='':
			idea = Idea.objects.get(pk = deleteid)
			if (request.user.is_superuser):
				idea.delete()
				messages.success(request,"Idea deleted")
			else:
				messages.error(request,"You can not delete any idea. You are not superuser.") 

	if request.method == 'GET':
				
		return render(request, 'ideas/main.html', {'ideas':ideas, 'filterform':filterlistideas_form})
	
	if request.method == 'POST':

		if filterlistideas_form.is_valid():
			if filter=='':
				ideas=Idea.objects.all()
			else:
				ideas=Idea.objects.all().filter(idea_title__icontains=filter)		
		
		return render(request, 'ideas/main.html', {'ideas':ideas, 'filterform':filterlistideas_form})


