import tweepy
import logging


logger = logging.getLogger()


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
            print e
            logger.info("Finish Digger from key: %s" % key)
            stream.disconnect()
    
    def get_actual_topic(self):
        return [self.topic.get_topic_like_hashtag()]

'''if __name__ == "__main__":
    print "Start Digger on " +time.strftime("%d/%m/%Y") + " at " +time.strftime("%H:%M:%S")
    a = Authenticator()
    d = Digger(a.authenticate())
    d.topic.saveConfiguration("Politica","obama") 
    d.startStreaming()'''
