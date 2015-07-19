'''
Created on 2/5/2015

@author: MacBook
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mole.settings'
import tweepy

from mole.app.domain.tweetPersistor import TweetPersistor
from mole.app.domain.hashtagPersistor import HashtagPersistor
from mole.app.models import Topic
from mole.app.domain.userPersistor import UserPersistor
# from app.domain import tasks

from mole.app.domain.task_followers import process_followers
from mole.app.utils import LoggerFactory

from mole.app.utils import StreamDAO, UserDAO, TweetDAO

from mole.app.domain.authenticator import Authenticator
from tweepy.api import API
from tweepy.error import TweepError

logger = LoggerFactory.create_logger()

class StreamProcessor():

    def __init__(self, api, async=False):
        
        self.stream_dao = StreamDAO()
        self.user_dao = UserDAO()
        self.tweet_dao = TweetDAO()
        self.count = 0
        self.api = api
        
    def start(self):
        
        records = self.stream_dao.find_to_process()
        for r in records:
            logger.info("About to process %s " % r['text'])
            cont = self.process(r)
            if not cont:
                break
        
    def get_followers(self,user_id):
        next_cursor = -1
        followers = []
            
        try: 
            cursor= tweepy.Cursor(self.api.followers_ids,user_id=user_id)
            for i in cursor.items():
                followers.append(i)
            next_cursor = cursor.iterator.next_cursor
        except TweepError as e:
            if e.response.status_code == 429:
                logger.info("Rate limit exceded! ")
                return False
            else:
                raise e
        logger.info("Next cursor is %d" % next_cursor)
        return followers

    def process(self, content):
        self.count += 1
        logger.info("Processing new record. Count is %d" % self.count)
        
        logger.info(content)
        if 'user' in content:
            user_content = content['user']
            user_id = user_content['id']
            user = self.user_dao.get(user_id)
            if not user:
                if not user_content['followers']:
                    followers = self.get_followers(user_id)
                    user_content['followers'] = followers
                self.user_dao.save(user_content)
            self.stream_dao.delete(content)
            self.tweet_dao.save(content)
            return True
        
            
            
        user_content = content['user']
        # ########## User ##############
        user_persistor = UserPersistor()
        logger.info("Start saving User")
        user = user_persistor.save_user(user_content)
        logger.info("User has been save successfully")
        
        #process_followers.delay(user=user, cursor=self.cursor)
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
        return True

if __name__ == '__main__':
    
    
    api = API(Authenticator().authenticate())
    sp = StreamProcessor(api)
    sp.start()