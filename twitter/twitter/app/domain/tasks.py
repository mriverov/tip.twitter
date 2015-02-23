from __future__ import absolute_import
import logging
import tweepy

from celery import Celery
from app.domain.authenticator import Authenticator
from app.domain.digger import Digger
from app.domain.stream import Stream
from app.domain.topicConfiguration import TopicConfiguration
from app.domain.followerPersistor import FollowerPersistor

celery_app = Celery('tasks', broker='amqp://guest@localhost//')

logger = logging.getLogger(__name__)


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


@celery_app.task(bind=True)
def start_digger(self, dominio, topic):
    logging.info("Celery task is going to be started with domain: " + dominio + "and topic " + topic)
    a = Authenticator()
    stream = Stream()
    topic_conf = TopicConfiguration()
    topic_conf.save_configuration(dominio, topic)
    digger = Digger(a.authenticate(), stream, topic_conf)
    try:
        digger.start_streaming(topic)
    except tweepy.TweepError, e:
        if tweepy.TweepError is "[{u'message': u'Over capacity', u'code': 130}]":
            logger.error("Error capacity Twitter: [{u'message': u'Over capacity', u'code': 130}])")
            logger.info("Waiting to try again")
            raise self.retry(exc=e, countdown=60 * 16)
    start_digger(dominio, topic)