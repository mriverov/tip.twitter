from django.db import models

# Create your models here.

class TweetUser(models.Model):
	user_id = models.BigIntegerField(null=True, blank=True)
	name = models.CharField(max_length=500, null=True, blank=True)
	screen_name = models.CharField(max_length=500, null=True, blank=True)
	description = models.CharField(max_length=500, null=True, blank=True)
	followers_count = models.IntegerField(null=True, blank=True)
	friends_count = models.IntegerField(null=True, blank=True)
	statuses_count = models.IntegerField(null=True, blank=True)
	favourites_count = models.IntegerField(null=True, blank=True)
	location = models.CharField(max_length=500, null=True, blank=True)
	time_zone = models.CharField(max_length=500, null=True, blank=True)
	created_at = models.DateTimeField(null=True, blank=True)
	
class Tweet(models.Model):
	tweetid = models.BigIntegerField(null=True, blank=True)
	text = models.CharField(max_length=5000, null=True, blank=True)
	favorite_count = models.IntegerField(null=True, blank=True)
	#hashtags_id = models.ForeignKey('Hashtag') TBD
	retweet_count = models.IntegerField(null=True, blank=True)
	#retweet_id = models.IntegerField(null=True, blank=True) TBD
	user = models.ForeignKey('TweetUser') 

class Hashtag(models.Model):
	text= models.CharField(max_length=100, null=True, blank=True)

