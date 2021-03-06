'''
Created on 2/5/2015

@author: MacBook
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mole.settings'
from datetime import datetime
import tweepy

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
            cursor = tweepy.Cursor(self.api.followers_ids, user_id = user_id)
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
        
        # logger.info(content)
        if 'user' in content:
            user_content = content['user']
            user_id = user_content['id']
            user = self.user_dao.get(user_id)
            if not user:
                followers = self.get_followers(user_id)
                user_content['followers'] = followers
                self.user_dao.save(user_content)
            self.stream_dao.delete(content)
            self.tweet_dao.save(content)
            return True

        return True

if __name__ == '__main__':
    api = API(Authenticator().authenticate())
    sp = StreamProcessor(api)
    sp.start()