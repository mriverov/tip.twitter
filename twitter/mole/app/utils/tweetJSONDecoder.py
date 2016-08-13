import logging
import json
import tweepy
from mole.app.exception.twitterExceptionHandler import TwitterExceptionHandler


__author__ = 'Marina'

logger = logging.getLogger(__name__)


class TweetJSONDecoder:

    def __init__(self):
        self.exception_handlder = TwitterExceptionHandler()

    def decode_tweet(self, content):
        try:
            info = [json.loads(content)]
            if self.exception_handlder.is_tweet_exception(info):
                logger.error(info)
                raise tweepy.TweepError(content)

            #logger.info("json decoded successfully: "+str(info))
        except ValueError as err:
            logger.error(err.message)
            #logger.error(content)
            info = self.decode_multiple_json(content)
            #logger.error(str(info))
        return info

    def decode_multiple_json(self, json_data):
        logger.info("Starting decoding multiple json")
        final_tweet_data = []
        json_tweet = json_data.split('\n')
        logger.info(json_tweet)
        for elem in json_tweet:
            decode_data = elem.encode('unicode_escape')
            if self.is_valid_data(decode_data):
                final_tweet_data.append(json.loads(elem))
        logger.info(str(final_tweet_data))
        return final_tweet_data

    def is_valid_data(self, elem):
        # hay otra forma de preguntar por string vacio
        return elem == ""








