import tweepy
import logging
import json
from app.domain.tweetPersistor import TweetPersistor
from app.domain.hashtagPersistor import HashtagPersistor
from app.models import Topic
from app.domain.userPersistor import UserPersistor
# from app.domain import tasks

# from twitter.app.domain.tasks import processFollowers
from app.utils.tweetJSONDecoder import TweetJSONDecoder

logger = logging.getLogger(__name__)


class Stream(tweepy.StreamListener):

    def __init__(self, max_data=30):
        self.buffer = ""
        self.max_data = max_data
        self.count = 0
        self.cursor = -1
        self.multiple_decoder = TweetJSONDecoder()

    @property
    def load_from_buffer(self):
        return self.multiple_decoder.decode_tweet(self.buffer)

    def on_data(self, data):
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
                # tasks.process_followers.delay(user=user, cursor=self.cursor)
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

    @staticmethod
    def get_topic():
        # se puede usar mientras tengamos un solo topico
        return Topic.objects.get()

    def on_error(self, status):
        logger.error("Error status is %s " % status)
        raise tweepy.TweepError(status)

    def reset_count(self):
        self.count = 0
