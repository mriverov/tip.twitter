import tweepy
import logging
import json
from twitter.app.domain.userPersistor import UserPersistor
from twitter.app.domain.tweetPersistor import TweetPersistor

logger = logging.getLogger()

class Stream(tweepy.StreamListener):
    
    def __init__(self):
        self.buffer = ""

    def on_data(self, data):
        logger.debug("New data arrived")
        print "-------------------"
        self.buffer += data
        if data.endswith("\r\n") and self.buffer.strip():
            content = json.loads(self.buffer)
            self.buffer = ""
            user_persistor = UserPersistor()
            user = user_persistor.saveUser(content['user']['name'], content['user']['description'])
            tweet = TweetPersistor()
            tweet.saveTweet(content['text'], content['id'], user)
            print content
            print "--------------"
        return True

    def on_error(self, status):
        logger.error("Error status is %s " %  status )
