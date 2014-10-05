from django.db import models

# Create your models here.

class Domain(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)

class Topic(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	count = models.IntegerField(null=True, blank=True, default=0)
	
	domain = models.ForeignKey('Domain')

class User(models.Model):
	user_id = models.BigIntegerField(null=True, blank=True)
	name = models.CharField(max_length=500, null=True, blank=True)
	screen_name = models.CharField(max_length=500, null=True, blank=True)
	description = models.CharField(max_length=1000, null=True, blank=True)
	followers_count = models.IntegerField(null=True, blank=True)
	friends_count = models.IntegerField(null=True, blank=True)
	statuses_count = models.IntegerField(null=True, blank=True)
	favourites_count = models.IntegerField(null=True, blank=True)
	location = models.CharField(max_length=500, null=True, blank=True)
	time_zone = models.CharField(max_length=500, null=True, blank=True)
	created_at = models.DateTimeField(null=True, blank=True)
	followers = models.ManyToManyField('self', related_name='followers', blank = True, null = True)
	
class Tweet(models.Model):
	tweetid = models.BigIntegerField(null=True, blank=True)
	text = models.CharField(max_length=5000, null=True, blank=True)
	favorite_count = models.IntegerField(null=True, blank=True)
	retweet_count = models.IntegerField(null=True, blank=True)
	retweet = models.ForeignKey('self', blank = True, null = True)
	author = models.ForeignKey('User') 
	topic = models.ForeignKey('Topic')
	user_mentions = models.ManyToManyField(User, related_name='mentions', blank = True, null = True)

class Hashtag(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	count = models.IntegerField(null=True, blank=True, default = 0)
	
	topic = models.ForeignKey('Topic')
	tweets = models.ManyToManyField(Tweet, related_name='hashtags', blank = True, null = True)



