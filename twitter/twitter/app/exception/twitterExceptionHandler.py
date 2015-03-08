import logging

__author__ = 'Marina'

logger = logging.getLogger(__name__)


class TwitterExceptionHandler:

    def __init__(self):
        self.general_expressions = ["{'limit':{'track':33}}", "{'limit':{'track':20}}"]

    @staticmethod
    def is_range_limit_outh_exception(expression):
        return expression is "Twitter error response: status code = 414"

    @staticmethod
    def is_information_not_found(expression):
        return expression is "[{u'message': u'Sorry, that page does not exist.', u'code': 34}]"

    @staticmethod
    def is_over_capacity_exception(expression):
        return expression is "Error capacity Twitter: [{u'message': u'Over capacity', u'code': 130}])"

    @staticmethod
    def is_range_limit_exception(expression):
        return expression is "Error status is 420"

    def is_general_tweet_limit_exception(self, expression):
        logger.info("Entro en geenral limit exception")
        logger.error(expression)
        return expression in self.general_expressions
