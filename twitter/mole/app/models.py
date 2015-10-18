import django
import os
from django.db import models

# Create your models here.

os.environ['DJANGO_SETTINGS_MODULE'] = 'mole.settings'
django.setup()

# class UserApp(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)
#     email = models.CharField(max_length=100, null=True, blank=True)
#     password = models.CharField(max_length=100, null=True, blank=True)


class Project(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    # user = models.ForeignKey('UserApp')


class KeyWord(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, default=0)
    project = models.ForeignKey('Project')


class Trend(models.Model):
    date = models.CharField(max_length=500, null=True, blank=True)
    tweets_count = models.IntegerField(null=True, blank=True, default=0)
    project = models.ForeignKey('Project')


class User(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    screen_name = models.CharField(max_length=500, null=True, blank=True, default="")
    followers_count = models.IntegerField(null=True, blank=True, default=0)
    location = models.CharField(max_length=500, null=True, blank=True, default="")
    centrality = models.FloatField(null=True, blank=True, default=0.0)

    followers = models.ManyToManyField('self', related_name='followers', blank=True, null=True)
#     followers = models.ManyToManyField('self',
#                                        through='Relationship',
#                                        symmetrical=False,
#                                        related_name='user_followers')
#
#     def add_relationship(self, other_user):
#         relationship, created = Relationship.objects.get_or_create(user=self, follower=other_user)
#         relationship.save()
#         return relationship
#
#
# class Relationship(models.Model):
#     user = models.ForeignKey('User', related_name='user')
#     follower = models.ForeignKey('User', related_name='follower')


class Tweet(models.Model):
    tweet_id = models.BigIntegerField(null=True, blank=True)
    text = models.CharField(max_length=5000, null=True, blank=True)
    retweet_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    retweet_id = models.BigIntegerField(null=True, blank=True)
    author = models.ForeignKey('User')
    project = models.ForeignKey('Project')
    trend = models.ForeignKey('Trend', null=True)
