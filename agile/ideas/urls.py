# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.user_login, name='login'),
    url(r'^signup', views.user_signup, name='signup'),
    url(r'^comment', views.submit_comment, name='comment'),
    url(r'^addIdea', views.add_idea, name='addIdea'),
]
