import time
import tweepy
import logging
from app.domain.authenticator import Authenticator
from app.domain.stream import Stream
from app.domain.topicConfiguration import TopicConfiguration


logger = logging.getLogger(__name__)


class Digger:

    def __init__(self, auth, stream, topic):
        self.auth = auth
        self.digger = stream
        self.topic = topic

    def tracking_keys(self):
        return self.get_actual_topic()

    def start_streaming(self, key):
        stream = tweepy.streaming.Stream(self.auth, self.digger)
        logger.info("Start streaming from key: %s" % key)
        try:
            stream.filter(track=key)
        except Exception as e:
            logger.error(e)
            logger.info("Finish Digger from key: %s" % key)
            stream.disconnect()
    
    def get_actual_topic(self):
        return [self.topic.get_topic_like_hashtag()]

'''if __name__ == "__main__":
    print "Start Digger on " + time.strftime("%d/%m/%Y") + " at " + time.strftime("%H:%M:%S")
    a = Authenticator()
    stream = Stream()
    topic_conf = TopicConfiguration()
    topic_conf.save_configuration("Barcelona", "malaga")
    digger = Digger(a.authenticate(), stream, topic_conf)
    digger.start_streaming("malaga")
'''