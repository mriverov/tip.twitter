import tweepy

from mole.app.utils.tweetJSONDecoder import TweetJSONDecoder

from mole.app.utils import StreamDAO, LoggerFactory

logger = LoggerFactory.create_logger()


class Stream(tweepy.StreamListener):

    def __init__(self, max_data=30000):
        self.buffer = ""
        self.max_data = max_data
        self.count = 0
        self.saved = 0
        self.cursor = -1
        self.topic = None
        self.multiple_decoder = TweetJSONDecoder()
        self.dao = StreamDAO()
        self.project = None

    @property
    def load_from_buffer(self):
        return self.multiple_decoder.decode_tweet(self.buffer)
    
    def on_data(self, data):
        # logger.info("New data arrived. Count is %d" % self.count)
        self.count += 1
        print "-------------------"
        # logger.info("Count is %d" % self.count)
        self.buffer = ""
        self.buffer += data
        try:
            if data.endswith("\r\n") and self.buffer.strip():
                tweet_data = self.load_from_buffer
                for content in tweet_data:

                    match = False
                    for keyword in self.topic:
                        if keyword in content['text'].lower() and (content['lang'] == 'es'):
                            content['project_id'] = self.project
                            self.dao.save(content)
                            match = True
                            break
                    if match:
                        self.saved += 1
                        logger.info("Matched: %s " % content['text'])
                    else:
                        logger.info("Not Matched : %s " % content['text'])
                            
                logger.info("Count is %d/%d" % (self.saved, self.count))
                if self.count >= self.max_data:
                    logger.info("Count: " + str(self.count) + "> max_data: " + str(self.max_data))
                    return False
        except Exception as e:
            logger.error(e)
        return True

    def set_topic(self, _topic):
        self.topic = _topic

    def set_project(self, project):
        self.project = project

    def on_error(self, status):
        logger.error("Error status is %s " % status)
        raise tweepy.TweepError(status)

    def reset_count(self):
        self.count = 0
