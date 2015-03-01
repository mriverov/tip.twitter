from __future__ import absolute_import
import logging
import tweepy

from celery import Celery
from app.domain.authenticator import Authenticator
from app.domain.digger import Digger
from app.domain.stream import Stream
from app.domain.topicConfiguration import TopicConfiguration
from app.domain.followerPersistor import FollowerPersistor
from app.exception.twitterExceptionHandler import TwitterExceptionHandler

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


# @celery_app.task(bind=True)
def start_digger(dominio, topic):
    """

    :rtype : digger
    """
    logging.info("Digger configuration for domain: " + dominio + "and topic " + topic)
    a = Authenticator()
    stream = Stream()
    topic_conf = TopicConfiguration()
    topic_conf.save_configuration(dominio, topic)
    digger = Digger(a.authenticate(), stream, topic_conf)
    return digger


@celery_app.task(bind=True)
def start_streaming(self, digger, topic):
    logging.info("Streaming is going to start for topic " + topic)
    try:
        digger.start_streaming(topic)
    except tweepy.TweepError as e:
        if exception_handlder.is_over_capacity_exception(tweepy.TweepError):
            logger.error(tweepy.TweepError)
            logger.info("Waiting to try again")
            raise self.retry(exc=e, countdown=60 * 16)
        if exception_handlder.is_information_not_found(tweepy.TweepError):
            logger.error(tweepy.TweepError)
            logger.info("Information not found ")
            raise self.retry(exc=e, countdown=1)
    except Exception as inst:
        if exception_handlder.is_range_limit_outh_exception(inst.message):
            logger.error(inst)
            logger.error("Error limit 414 from twitter has been stoped the streaming, waiting for permission ")
            raise self.retry(exc=inst, countdown=60 * 16)
        if exception_handlder.is_range_limit_exception(inst.message):
            logger.error(inst)
            logger.error("Error limit 420 from twitter has been stoped the streaming, waiting for restart limit ")
        logger.info("Si llego hasta aca es porque no agarro por ningun error anterior")
        logger.error(inst.message)
    # Comente esto para probar si es lo que esta generando el maximum recursion depth exceeded.
    digger.reset()
    start_streaming(digger, topic)