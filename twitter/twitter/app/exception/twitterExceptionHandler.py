import logging

__author__ = 'Marina'

logger = logging.getLogger(__name__)


class TwitterExceptionHandler:

    """
    Process exceptions:
    {'message': 'Over capacity', 'code': 130}
    {'message': 'Sorry, that page does not exist.', 'code': 34}
    {'message': 'Rate limit exceeded', 'code': 88},

    {'limit':{'track':33}},
    {'limit':{'track':20}},
    {'limit': {'track': 233}},
    {'limit': {'track': 1}},
    {'limit': {'track': 31}}
    """

    def __init__(self):
        pass

    @staticmethod
    def is_range_limit_outh_exception(expression):
        return expression == "Twitter error response: status code = 414"

    @staticmethod
    def is_range_limit_exception(expression):
        return expression == "420"

    def is_limit_exception(self, expression):
        return self.is_exception_of(expression, 'limit')

    def is_message_limit_exception(self, expression):
        if self.is_exception_of(expression, 'message'):
            message = expression[0]['message']
            message = message.encode('unicode_escape')
            return message == ' Over capacity' or message=='Rate limit exceeded'

    def page_does_not_exist(self, expression):
        if self.is_exception_of(expression, 'message'):
            message = expression[0]['message']
            message = message.encode('unicode_escape')
            return message == 'Sorry, that page does not exist.'

    def is_exception_of(self, expression, exception_key):
        logger.error(expression)
        logger.error(exception_key)
        if type(expression) == type(list()):
            value = expression[0]

        if self.is_tweet_exception_type(value):
            keys = value.keys()
            logger.info("Keys: "+str(keys))
            for key in keys:
                key_d = key.encode('unicode_escape')
                logger.info("key id: "+str(key_d))
                return key_d in [exception_key]
        return False

    @staticmethod
    def is_tweet_exception_type(expression):
        return type(expression) == type(dict())

    def is_tweet_exception(self, value):
        return self.is_limit_exception(value) or self.is_message_limit_exception(value)