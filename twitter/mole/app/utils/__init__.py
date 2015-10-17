from logging import FileHandler
import datetime
__author__ = 'Marina'

import coloredlogs
import logging
import traceback

#from requests.packages.urllib3 import  disable_warnings

from pymongo import MongoClient

HOST="bati"
class MongoDAO():
    
    def __init__(self):
        self.mongo = MongoClient(host=HOST)

    def save(self, data):
        self.col.insert_one(data)

    def delete(self,data):
        self.col.delete_one({'_id': data['_id'] })
        
    def update(self,_id, content):
        self.col.update_one({'_id':_id}, {'$set':content})
        
class StreamDAO(MongoDAO):
    
    def __init__(self):
        MongoDAO.__init__(self)
        self.col = self.mongo.mole.stream
        
    def find_to_process(self):
        records = self.mongo.mole.stream.find().limit(1000)
        return records
    
class UserDAO(MongoDAO):
    
    def __init__(self):
        MongoDAO.__init__(self)
        self.col = self.mongo.mole.user
    
    def get(self,id):
        user = self.col.find_one({'id':id})
        return user 

class TweetDAO(MongoDAO):
    
    def __init__(self):
        MongoDAO.__init__(self)
        self.col = self.mongo.mole.tweet 

class ErrorHandler:
    
    def __init__(self):
        
        #disable_warnings()

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
# 	           disable_warnings()
            coloredlogs.install()
            FORMAT = '%(asctime)-15s-8s %(message)s'
            logging.basicConfig(fomat=FORMAT)
            
            logger = logging.getLogger(name)
            logfile_name = "%s.txt" % datetime.datetime.now().isoformat("T")
            fh = FileHandler(logfile_name)
            logger.addHandler(fh)

            logger.setLevel(logging.DEBUG)

            logger.info("Mole Logger initialized")
            
            LoggerFactory.default_logger = logger
        
        return LoggerFactory.default_logger
