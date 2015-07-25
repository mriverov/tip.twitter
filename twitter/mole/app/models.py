from django.db import models

# Create your models here.


class Domain(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)


class Topic(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, default=0)

    domain = models.ForeignKey('Domain')


class Hashtag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, default=0)

    topic = models.ForeignKey('Topic')



