from django.shortcuts import render

# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.sites.models import Site
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

@require_http_methods(["GET"])
def index(request):
	return render (request, 'ideas/index.html')

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
        return render_to_response('comments.html', {'form': CommentForm,
                'allow_comments':True,
            }, context_instance=RequestContext(request))
         messages.error(request, "You don't have commented")
    else:
return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
