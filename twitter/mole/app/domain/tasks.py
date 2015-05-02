from __future__ import absolute_import
import logging

from celery import Celery
from app.domain.authenticator import Authenticator
from app.domain.digger import Digger
from app.domain.stream import Stream
from app.domain.topicConfiguration import TopicConfiguration
from app.exception.twitterExceptionHandler import TwitterExceptionHandler

celery_app = Celery('tasks', broker='amqp://guest@localhost//')

logger = logging.getLogger(__name__)

exception_handlder = TwitterExceptionHandler()


# @celery_app.task(bind=True)
def start_digger(dominio, keyword, mention, hashtag):
    """

    :rtype : digger
    """
    logging.info("Digger configuration for domain: " + dominio + "and topic " + keyword)
    a = Authenticator()
    stream = Stream()
    topic_conf = TopicConfiguration()
    topic_conf.save_configuration(dominio, keyword, mention, hashtag)
    digger = Digger(a.authenticate(), stream)
    return digger


@celery_app.task(bind=True)
def start_streaming(self, digger, topic, **kwargs):
    logging.info("Streaming is going to start for topic " + topic)
    try:
        digger.start_streaming(topic)
    except Exception as e:
        logger.error(e.message)
        if exception_handlder.is_message_limit_exception(e.message) or exception_handlder.is_message_limit_exception(
                e.message):
            logger.info("Waiting to try again")
            raise self.retry(exc=e, countdown=10)
            # self.retry(args=[digger, topic], exc=e, countdown=10)
        if exception_handlder.page_does_not_exist(e.message):
            logger.info("Information not found ")
            # raise self.retry(exc=e, countdown=10)
            self.retry(args=[digger, topic], exc=e, countdown=10)
        if exception_handlder.is_range_limit_outh_exception(e.message):
            logger.error("Error limit 414 from twitter has been stoped the streaming, waiting for permission ")
            # raise self.retry(exc=e, countdown=10)
            self.retry(args=[digger, topic], exc=e, countdown=10)
        if exception_handlder.is_range_limit_exception(e.message):
            logger.error("Error limit 420 from twitter has been stoped the streaming, waiting for restart limit ")
            self.retry(args=[digger, topic], exc=e, countdown=10)

        logger.info("Si llego hasta aca es porque no agarro por ningun error anterior")
        raise self.retry(args=[digger, topic], exc=e, countdown=10)
    digger.reset()
    start_streaming(digger, topic)