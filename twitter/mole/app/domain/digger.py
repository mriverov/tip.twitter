import tweepy
import logging


from mole.app.exception.twitterExceptionHandler import TwitterExceptionHandler
from mole.app.domain.authenticator import Authenticator
from mole.app.domain.stream import Stream

from mole.app.utils import LoggerFactory, ErrorHandler
from pygments.lexers._postgres_builtins import KEYWORDS

logger = LoggerFactory.create_logger()

handler =ErrorHandler()

class Digger:

    def __init__(self, auth, stream):
        self.auth = auth
        self.digger = stream
        self.exception_handlder = TwitterExceptionHandler()

    def start_streaming(self, keywords):
        self.digger.set_topic(keywords)
        stream = tweepy.streaming.Stream(self.auth, self.digger)
        logger.info("Start streaming from key: %s" % keywords)
        try:
            #stream.filter(track=keywords,locations=[-73.533,-58.583,-53.367,-21.783 ])
            stream.filter(track=keywords)
        except tweepy.TweepError as e:
            handler.handle_error(e)
            raise e
        except Exception as inst:
            handler.handle_error(inst)
            logger.info("Finish Digger from key: %s" % key)
            stream.disconnect()
            raise inst

    def reset(self):
        self.digger.reset_count()

if __name__ == '__main__':
    
    logging.basicConfig()
    
    a = Authenticator()
    
    stream = Stream()

    digger = Digger(a.authenticate(), stream)
    digger.start_streaming(['scioli','massa','carrio','cfk'])