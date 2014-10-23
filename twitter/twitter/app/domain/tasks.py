import logging
import tweepy

from celery import Celery
from twitter.app.domain.authenticator import Authenticator
from twitter.app.domain.digger import Digger
from twitter.app.domain.followerPersistor import FollowerPersistor

celery_app = Celery('tasks', broker='amqp://guest@localhost//')

logger = logging.getLogger()

@celery_app.task(bind=True)
def processFollowers(self, user, cursor):
	logger.info("New task 'processFollowers from user: %s" %user.name) 
	next_cursor = None
	try:
		if cursor == 0:
			return "Finished processing followers of %s" %user.name
		next_cursor = FollowerPersistor().processFollowersFrom(user, cursor)
	except tweepy.error.TweepError as exc:
		logger.info("Exceeded limit... Waiting...")
		raise self.retry(exc=exc, countdown=60*16)
	
	processFollowers.s(user, next_cursor)
	
@celery_app.task(bind=True)
def startDigger(self, key):
	a = Authenticator()
	d = Digger(a.authenticate())
	d.startStreaming(key)


