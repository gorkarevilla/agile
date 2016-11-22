#from __future__ import unicode_literals

# Create your models here.
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Idea(models.Model):
    idea_title = models.CharField(max_length=50, validators=[MinLengthValidator(3, message='Length has to be more than 3')])
    idea_text = models.TextField(max_length=500, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

# Comment Ideas Model
class Comment(models.Model):
    idea_id = models.ForeignKey(Idea, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=80)
    comment = models.TextField()
