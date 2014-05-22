from django.db import models

# Create your models here.

class TweetUser(models.Model):

	name = models.CharField(max_length=500, null=True, blank=True)

	description = models.CharField(max_length=500, null=True, blank=True)

