import logging
import json


__author__ = 'Marina'

logger = logging.getLogger(__name__)


class TweetJSONDecoder:

    def __init__(self):
        pass

    def decode_tweet(self, content):
        try:
            info = [json.loads(content)]
        except ValueError as err:
            logger.error(err)
            logger.error(err.message)
            logger.error("Se rompio json")
            logger.error(content)
            info = self.decode_multiple_json(content)
            logger.error("Se decodifico json")
            logger.error(str(info))
        return info

    def decode_multiple_json(self, json_data):
        final_tweet_data = []
        json_tweet = json_data.split('\n')
        logger.info(json_tweet)
        logger.info(" AAAAAAAAAAAAAAAAAH")
        for elem in json_tweet:
            decode_data = elem.encode('utf-8')
            if self.is_valid_data(decode_data):
                final_tweet_data.append(json.loads(elem))
        logger.info(str(final_tweet_data))
        return final_tweet_data

    def is_valid_data(self, elem):
        # hay otra forma de preguntar por string vacio
        return elem == ""








