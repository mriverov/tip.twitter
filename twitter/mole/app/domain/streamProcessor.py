'''
Created on 2/5/2015

@author: MacBook
'''

import tweepy

from mole.app.domain.tweetPersistor import TweetPersistor
from mole.app.domain.hashtagPersistor import HashtagPersistor
from mole.app.models import Topic
from mole.app.domain.userPersistor import UserPersistor
# from app.domain import tasks

from mole.app.domain.task_followers import process_followers
from mole.app.utils import LoggerFactory

from mole.app.utils import StreamDAO

logger = LoggerFactory.create_logger()

class StreamProcessor():

    def __init__(self,async=False):
        
        self.dao = StreamDAO()
        
    def start(self):
        
        records = self.dao.find_to_process()
        for r in records:
            logger.info("About to process %s " % r['text'])
            self.process(r)

    def process(self, content):
        logger.info("Processing new record. Count is %d" % self.count)
        self.count += 1
        logger.info(content)
        user_content = content['user']
        # ########## User ##############
        user_persistor = UserPersistor()
        logger.info("Start saving User")
        user = user_persistor.save_user(user_content)
        logger.info("User has been save successfully")
        
        process_followers.delay(user=user, cursor=self.cursor)
        # ######### Tweet ##############
        tweet_persistor = TweetPersistor()
        logger.info("Start saving Tweet")
        tweet = tweet_persistor.save_tweet(content, self.get_topic(), user, user_persistor)
        logger.info("Tweet has been save successfully")
        # ######## Hashtag #############
        hashtag_info = content['entities']['hashtags']
        hashtag = HashtagPersistor()
        logger.info("Start saving Hashtag")
        hashtag.save_hashtag(hashtag_info, self.get_topic(), tweet)
        logger.info("Hashtag has been save successfully")
        logger.info("--------------")

    def set_topic(self, _topic):
        self.topic = _topic

    def on_error(self, status):
        logger.error("Error status is %s " % status)
        raise tweepy.TweepError(status)

    def reset_count(self):
        self.count = 0

    def get_topic(self):
        return Topic.objects.get(name=self.topic)


if __name__ == '__main__':
    
    sp = StreamProcessor()
    sp.start()