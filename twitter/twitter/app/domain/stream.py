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
        logger.info("New data arrived")
        print "-------------------"
        self.buffer += data
        if data.endswith("\r\n") and self.buffer.strip():
            content = json.loads(self.buffer)       
            user_content = content['user']
            user_persistor = UserPersistor()
            user = user_persistor.saveUser(user_content['id'],user_content['name'], user_content['screen_name'], user_content['description'], 
                                           user_content['followers_count'], user_content['friends_count'], user_content['statuses_count'],
                                           user_content['favourites_count'], user_content['location'], user_content['time_zone'],
                                           user_content['created_at'])
            
            tweet = TweetPersistor()
            tweet.saveTweet(content['id'], content['text'],content['favorite_count'], 
                            content['retweet_count'], user)
            
            self.buffer = ""
            print "--------------"
        return True

    def on_error(self, status):
        logger.error("Error status is %s " %  status )
