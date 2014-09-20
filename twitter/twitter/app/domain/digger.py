import tweepy
import stream
import time
import datetime
from twitter.app.domain.authenticator import Authenticator
from twitter.app.domain.topicConfiguration import TopicConfiguration

class Digger:

    def __init__(self, auth):
        self.auth = auth
        self.digger = stream.Stream()
        self.topic = TopicConfiguration()
        self.start = None
        self.end = None

    def trackingKeys(self):
        return self.getActualTopic()

    def startStreaming(self):   
        stream = tweepy.streaming.Stream(self.auth, self.digger)
        print "Streaming started..."
        try:
            stream.filter(track=self.trackingKeys())
            #stream.filter(follow=['38744894'])
        except Exception as e:
            print e
            print "Finish Digger on " +time.strftime("%d/%m/%Y") + " at " +time.strftime("%H:%M:%S")
            self.end = datetime.datetime.now().replace(microsecond=0)
            print "The streaming process was for" +self.end - self.start
            stream.disconnect()
    
    def getActualTopic(self):
        key = []
        key.append(self.topic.getTopicLikeHashtag())
        return key
        

            
if __name__ == "__main__":
    print "Start Digger on " +time.strftime("%d/%m/%Y") + " at " +time.strftime("%H:%M:%S")
    a = Authenticator()
    d = Digger(a.authenticate())
    d.topic.saveConfiguration("Deporte","premierLeague") 
    d.start = datetime.datetime.now().replace(microsecond=0)
    d.startStreaming()
