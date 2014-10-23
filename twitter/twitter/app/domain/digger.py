import tweepy
import stream
import logging

#from twitter.app.domain.authenticator import Authenticator
from twitter.app.domain.topicConfiguration import TopicConfiguration

logger = logging.getLogger()

class Digger:

    def __init__(self, auth):
        self.auth = auth
        self.digger = stream.Stream()
        self.topic = TopicConfiguration()

    def trackingKeys(self):
        return self.getActualTopic()

    def startStreaming(self, key):   
        stream = tweepy.streaming.Stream(self.auth, self.digger)
        logger.info("Start streaming from key: %s" %key) 
        try:
            stream.filter(track=key)
        except Exception as e:
            print e
            logger.info("Finish Digger from key: %s" %key)
            stream.disconnect()
    
    def getActualTopic(self):
        key = []
        key.append(self.topic.getTopicLikeHashtag())
        return key
        
            
'''if __name__ == "__main__":
    print "Start Digger on " +time.strftime("%d/%m/%Y") + " at " +time.strftime("%H:%M:%S")
    a = Authenticator()
    d = Digger(a.authenticate())
    d.topic.saveConfiguration("Politica","obama") 
    d.startStreaming()'''
