import tweepy
import logging
import json
from twitter.app.domain.tweetPersistor import TweetPersistor
from twitter.app.domain.hashtagPersistor import HashtagPersistor
from twitter.app.models import Topic
from twitter.app.domain.userPersistor import UserPersistor

logger = logging.getLogger()

def processFollowers():
	pass

class Stream(tweepy.StreamListener):
    
    def __init__(self,max_data=100, processFollowers=processFollowers):
        self.buffer = ""
        self.max_data = max_data
        self.count = 0

    def on_data(self, data):
        logger.info("New data arrived. Count is %d" % self.count)
        self.count+=1
        print "-------------------"
        self.buffer += data
        if data.endswith("\r\n") and self.buffer.strip():
            content = json.loads(self.buffer)  
            print data     
            user_content = content['user']
            
            ########### User ##############
            user_persistor = UserPersistor()
            user = user_persistor.saveUser(user_content)
            processFollowers.delay(user=user, cursor=-1)    
            ########## Tweet ##############
            tweet_persistor = TweetPersistor()
            tweet = tweet_persistor.saveTweet(content, self.getTopic(), user, user_persistor)
            print "tweet"
            
            ######### Hashtag #############
            hastag_info = content['entities']['hashtags']
            hashtag = HashtagPersistor()
            hashtag.saveHashtag(hastag_info, self.getTopic(), tweet)
            
            self.buffer = ""
            print "--------------"
            if self.count >= self.max_data:
                logger.info("Count: %d > max_data: %d" % self.count, self.max_data)
                return False
        return True
    
    def getTopic(self):
        # se puede usar mientras tengamos un solo topico
        return Topic.objects.get()

    def on_error(self, status):
        logger.error("Error status is %s " %  status )
