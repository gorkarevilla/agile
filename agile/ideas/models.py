#from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Idea(models.Model):
    idea_title = models.CharField(max_length=50)
    idea_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


# Comment Ideas Model
class Comment(models.Model):
    idea_id = models.ForeignKey('Ideas',
                                db_column='idea_id',
                                blank=False,
                                null=False,
                                related_name='comments')
    user_name = models.CharField(max_length=80)
    comment = models.TextField()
