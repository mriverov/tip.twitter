from __future__ import absolute_import
import logging
import tweepy

from celery import Celery
from mole.app.domain.followerPersistor import FollowerPersistor
from mole.app.exception.twitterExceptionHandler import TwitterExceptionHandler

celery_app = Celery('tasks', broker='amqp://guest@localhost//')

logger = logging.getLogger(__name__)

exception_handlder = TwitterExceptionHandler()

@celery_app.task(bind=True)
def process_followers(self, user, cursor):
    logger.info("New task 'processFollowers from user: %s" % user.name)
    try:
        if cursor == 0:
            return "Finished processing followers of %s" % user.name
        next_cursor = FollowerPersistor().process_followers_from(user, cursor)
    except tweepy.error.TweepError as exc:
        logger.info("Exceeded limit... Waiting...")
        raise self.retry(exc=exc, countdown=60 * 16)
    process_followers(user, next_cursor)