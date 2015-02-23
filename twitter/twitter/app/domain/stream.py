import tweepy
import logging
import json
from app.domain.tweetPersistor import TweetPersistor
from app.domain.hashtagPersistor import HashtagPersistor
from app.models import Topic
from app.domain.userPersistor import UserPersistor
# from app.domain import tasks

# from twitter.app.domain.tasks import processFollowers

logger = logging.getLogger()


class Stream(tweepy.StreamListener):

    def __init__(self, max_data=100):
        self.buffer = ""
        self.max_data = max_data
        self.count = 0
        self.cursor = -1

    def on_data(self, data):
        logger.info("New data arrived. Count is %d" % self.count)
        self.count += 1
        print "-------------------"
        self.buffer += data
        if data.endswith("\r\n") and self.buffer.strip():
            content = json.loads(self.buffer)
            print data
            user_content = content['user']

            ########### User ##############
            user_persistor = UserPersistor()
            user = user_persistor.save_user(user_content)
            #tasks.process_followers.delay(user=user, cursor=self.cursor)
            ########## Tweet ##############
            tweet_persistor = TweetPersistor()
            tweet = tweet_persistor.save_tweet(content, self.get_topic(), user, user_persistor)
            print "tweet"

            ######### Hashtag #############
            hashtag_info = content['entities']['hashtags']
            hashtag = HashtagPersistor()
            hashtag.save_hashtag(hashtag_info, self.get_topic(), tweet)

            self.buffer = ""
            print "--------------"
            if self.count >= self.max_data:
                logger.info("Count: %d > max_data: %d" % self.count, self.max_data)
                return False
        return True

    @staticmethod
    def get_topic():
        # se puede usar mientras tengamos un solo topico
        return Topic.objects.get()

    def on_error(self, status):
        logger.error("Error status is %s " % status)
