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

logger = LoggerFactory.create_logger()


class StreamProcessor():


    def on_data2(self, data):
        logger.info("New data arrived. Count is %d" % self.count)
        self.count += 1
        print "-------------------"
        logger.info("Count is %d" % self.count)
        self.buffer = ""
        self.buffer += data
        if data.endswith("\r\n") and self.buffer.strip():
            tweet_data = self.load_from_buffer
            for content in tweet_data:
                logger.info("Start saving information")
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
            logger.info("Count is %d" % self.count)
            if self.count >= self.max_data:
                logger.info("Count: " + str(self.count) + "> max_data: " + str(self.max_data))
                return False
        return True

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
    pass