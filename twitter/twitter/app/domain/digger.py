import tweepy
import logging
from app.exception.twitterExceptionHandler import TwitterExceptionHandler


logger = logging.getLogger(__name__)


class Digger:

    def __init__(self, auth, stream, topic):
        self.auth = auth
        self.digger = stream
        self.topic = topic
        self.exception_handlder = TwitterExceptionHandler()

    def tracking_keys(self):
        return self.get_actual_topic()

    def start_streaming(self, key):
        stream = tweepy.streaming.Stream(self.auth, self.digger)
        logger.info("Start streaming from key: %s" % key)
        try:
            stream.filter(track=key)
        except tweepy.TweepError as e:
            logger.info("Es un error de twitter")
            raise e
        except Exception as inst:
            logger.error(inst.message)
            logger.error(inst)
            logger.info("Finish Digger from key: %s" % key)
            stream.disconnect()

    def reset(self):
        self.digger.reset_count()

    def get_actual_topic(self):
        return [self.topic.get_topic_like_hashtag()]
