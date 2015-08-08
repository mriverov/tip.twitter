from django.db import models

# Create your models here.


class UserApp(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)


class Project(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    # user = models.ForeignKey('UserApp')


class KeyWord(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, default=0)

    project = models.ForeignKey('Project')


class User(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    screen_name = models.CharField(max_length=500, null=True, blank=True)
    followers_count = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    followers = models.ManyToManyField('self', related_name='followers', blank=True, null=True)
    centrality = models.FloatField(null=True, blank=True, default=0.0)


class Tweet(models.Model):
    tweet_id = models.BigIntegerField(null=True, blank=True)
    text = models.CharField(max_length=5000, null=True, blank=True)
    retweet_count = models.IntegerField(null=True, blank=True)
    retweet_id = models.BigIntegerField(null=True, blank=True)
    author = models.ForeignKey('User')
    project = models.ForeignKey('Project')
