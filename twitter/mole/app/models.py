import django
import os
from django.db import models

# Create your models here.

os.environ['DJANGO_SETTINGS_MODULE'] = 'mole.settings'
# django.setup()

class Project(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

class KeyWord(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, default=0)
    project = models.ForeignKey('Project')

class Trend(models.Model):
    date = models.CharField(max_length=500, null=True, blank=True)
    tweets_count = models.IntegerField(null=True, blank=True, default=0)
    project = models.ForeignKey('Project')

class User(models.Model):
    user_id = models.BigIntegerField(db_index=True, null=True, blank=True)
    screen_name = models.CharField(max_length=500, null=True, blank=True, default="")
    followers_count = models.IntegerField(null=True, blank=True, default=0)
    location = models.CharField(max_length=500, null=True, blank=True, default="")
    centrality = models.FloatField(null=True, blank=True, default=0.0)
    followers = models.ManyToManyField('self', related_name='followers', blank=True, null=True)

class Tweet(models.Model):
    tweet_id = models.BigIntegerField(null=True, blank=True)
    text = models.CharField(max_length=5000, null=True, blank=True)
    retweet_count = models.IntegerField(null=True, blank=True)
    favorite_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    retweet_id = models.BigIntegerField(null=True, blank=True)
    author = models.ForeignKey('User')
    project = models.ForeignKey('Project')
    trend = models.ForeignKey('Trend', null=True)

class Urls(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    url = models.CharField(max_length=5000, null=True, blank=True)

class UrlsGraph(models.Model):
    user_oid_i = models.BigIntegerField(null=True, blank=True)
    user_oid_j = models.BigIntegerField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True, default=0.0)

class CentralityUrl(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    centrality = models.FloatField(null=True, blank=True, default=0.0)


class Hashtag(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    hashtag = models.CharField(max_length=5000, null=True, blank=True)


class HashtagGraph(models.Model):
    user_oid_i = models.BigIntegerField(null=True, blank=True)
    user_oid_j = models.BigIntegerField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True, default=0.0)


class CentralityHashtag(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    centrality = models.FloatField(null=True, blank=True, default=0.0)


