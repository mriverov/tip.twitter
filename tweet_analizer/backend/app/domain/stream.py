import tweepy
from userPersistor import UserPersistor
from tweetPersistor import TweetPersistor
import logging
import json

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
            #print content            
            self.buffer = ""
            user = UserPersistor()
            print '****Usuario:' + content['user']['name'] + ' ********Desc:' + content['user']['description'] 
            user.saveUser(content['user']['name'], content['user']['description'])
            tweet = TweetPersistor()
            # print '****Tweet:' + content['text'] + ' ********ID:' + content['id']
            tweet.saveTweet(content['text'], content['id'])
            #print content['user']['name']
            #print content['user']['name']
            #print content['user']['time_zone']
            #print content['text']
            #print content['encoding']
            #print content
            print "New data persisted"
            #logger.debug("ID is %s " % data['id'])
            #logger.debug("Text is %s " % data['text'])
        #logger.debug("Data is: %s " % data)
        return True

    def on_error(self, status):
        logger.error("Error status is %s " %  status )
