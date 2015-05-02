__author__ = 'Marina'

import coloredlogs
import logging
import traceback

from requests.packages.urllib3 import  disable_warnings

from pymongo import MongoClient

class StreamDAO:
    
    def __init__(self):
        self.mongo = MongoClient()
    
    def save(self, data):
        
        self.mongo.mole.stream.insert_one(data)

class ErrorHandler:
    
    def __init__(self):
        
        disable_warnings()

        lf = LoggerFactory()
        self.logger = lf.create_logger()

    def handle_error(self, e):
        self.logger.error(e)
        self.logger.error(traceback.format_exc())


class LoggerFactory:
    default_logger = None

    @classmethod
    def create_logger(cls, name='mole'):
        
        if not LoggerFactory.default_logger:
            disable_warnings()
            coloredlogs.install()
            FORMAT = '%(asctime)-15s-8s %(message)s'
            logging.basicConfig(fomat=FORMAT)
            
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            
            logger.info("Mole Logger initialized")
            
            LoggerFactory.default_logger = logger
        
        return LoggerFactory.default_logger
