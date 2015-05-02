import logging
from mole.app.models import Hashtag

logger = logging.getLogger(__name__)


class HashtagPersistor:
    
    def __init__(self):
        pass

    @staticmethod
    def save_hashtag(hashtag, _topic, tweet):
        if hashtag:
            hashtag_list = hashtag[0]
            if hashtag_list:
                if 'text' in hashtag_list:
                    _name = hashtag_list['text']
                    if _name is not None:
                        _name = _name.encode('unicode_escape')
                    hashtag_list = Hashtag(name=_name, topic=_topic)
                    hashtag_list.save()
                    hashtag_list.tweets.add(tweet)
                    hashtag_list.save()