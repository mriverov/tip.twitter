import tweepy

import logging
import json

logger = logging.getLogger()

class Stream(tweepy.StreamListener):
    
    def __init__(self):
        self.buffer = ""

    def on_data(self, data):
        logger.debug("New data arrived")
        self.buffer += data
        if data.endswith("\r\n") and self.buffer.strip():
            content = json.loads(self.buffer)
            self.buffer = ""
            print content['user']['id']
            print content['user']['name']
            print content['user']['time_zone']
            print content['text']
            #print content['encoding']
            print "--------------"
            #logger.debug("ID is %s " % data['id'])
            #logger.debug("Text is %s " % data['text'])
        #logger.debug("Data is: %s " % data)
        return True

    def on_error(self, status):
        logger.error("Error status is %s " %  status )
