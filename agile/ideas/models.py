from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Idea(models.Model):
    idea_title = models.CharField(max_length=50)
    idea_text = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
