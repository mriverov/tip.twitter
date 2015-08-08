import logging

from mole.app.models import Tweet

logger = logging.getLogger(__name__)


class TweetPersistor:
    
    def __init__(self):
        pass

    def save_tweet(self, content, project, user):
        text = content['text']
        retweet_id = None
        if 'retweeted_status' in content and content['retweeted_status'] is not None:
            retweet_id = content['retweeted_status']['id']
        if text is not None:
            text = text.encode('unicode_escape')
        tweet = Tweet(tweet_id=content['id'], text=text, retweet_count=content['retweet_count'], author=user,
                      project=project, retweet_id=retweet_id)
        return tweet.save()


