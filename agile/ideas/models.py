from __future__ import unicode_literals

from django.db import models

# Comment Ideas Model 
class Comment(models.Model):
    idea_id= models.ForeignKey('Ideas',db_column='idea_id', blank=False, null=False, related_name='comments')
    user_name = models.CharField(max_length=80)
    comment = models.TextField()
