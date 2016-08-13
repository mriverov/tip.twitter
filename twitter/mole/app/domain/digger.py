import tweepy
import logging


# from mole.app.exception.twitterExceptionHandler import TwitterExceptionHandler
from mole.app.domain.authenticator import Authenticator
from mole.app.domain.stream import Stream

from mole.app.utils import LoggerFactory, ErrorHandler

logger = LoggerFactory.create_logger()

handler = ErrorHandler()


class Digger:

    def __init__(self, auth, stream):
        self.auth = auth
        self.digger = stream
        # self.exception_handlder = TwitterExceptionHandler()

    def start_streaming(self, keywords, project=None):
        self.digger.set_topic(keywords)
        self.digger.set_project(project)
        stream = tweepy.streaming.Stream(self.auth, self.digger, gzip=True)
        logger.info("Start streaming from key: %s" % keywords)
        try:
            # stream.filter(track=keywords,locations=[-73.533,-58.583,-53.367,-21.783 ])
            stream.filter(track=keywords)
        except tweepy.TweepError as e:
            handler.handle_error(e)
            raise e
        except Exception as inst:
            handler.handle_error(inst)
            logger.info("Finish Digger from key: %s" % keywords)
            stream.disconnect()
            raise inst

    def reset(self):
        self.digger.reset_count()

    @staticmethod
    def start_digger(keywords, project):
        logging.basicConfig()
        a = Authenticator()
        stream = Stream()
        digger = Digger(a.authenticate(), stream)
        digger.start_streaming(keywords, project)

if __name__ == '__main__':
    logging.basicConfig()
    a = Authenticator()
    stream = Stream()
    digger = Digger(a.authenticate(), stream)
    digger.start_streaming(['scioli','macri','cfk'])