__author__ = 'Marina'


class TwitterExceptionHandler:

    def __init__(self):
        pass

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

