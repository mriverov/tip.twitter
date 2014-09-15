import tweepy
import stream
from twitter.app.domain.authenticator import Authenticator
from twitter.app.domain.topicConfiguration import TopicConfiguration

class Digger:

    def __init__(self, auth):
        self.auth = auth
        self.digger = stream.Stream()
        self.topic = TopicConfiguration()

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
            stream.disconnect()
    
    def getActualTopic(self):
        key = []
        key.append(self.topic.getTopicLikeHashtag())
        return key
        

            
if __name__ == "__main__":
    a = Authenticator()
    d = Digger(a.authenticate())
    d.topic.saveConfiguration("Deporte","premierLeague") 
    d.startStreaming()
