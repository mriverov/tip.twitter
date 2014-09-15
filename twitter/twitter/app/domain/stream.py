import tweepy
import logging
import json
from twitter.app.domain.userPersistor import UserPersistor
from twitter.app.domain.tweetPersistor import TweetPersistor
from twitter.app.domain.hashtagPersistor import HashtagPersistor
from twitter.app.models import Topic

logger = logging.getLogger()

class Stream(tweepy.StreamListener):
    
    def __init__(self):
        self.buffer = ""

    def on_data(self, data):
        logger.info("New data arrived")
        print "-------------------"
        self.buffer += data
        if data.endswith("\r\n") and self.buffer.strip():
            content = json.loads(self.buffer)  
            print data     
            user_content = content['user']
            
            ########### User ##############
            user_persistor = UserPersistor()
            user = user_persistor.saveUser(user_content)
            
            ########## Tweet ##############
            tweet_persistor = TweetPersistor()
            tweet = tweet_persistor.saveTweet(content, self.getTopic(), user, user_persistor)
            
            ######### Hashtag #############
            hastag_info = content['entities']['hashtags']
            hashtag = HashtagPersistor()
            hashtag.saveHashtag(hastag_info, self.getTopic(), tweet)
            
            self.buffer = ""
            print "--------------"
        return True
    
    def getTopic(self):
        # se puede usar mientras tengamos un solo topico
        return Topic.objects.get()

    def on_error(self, status):
        logger.error("Error status is %s " %  status )
