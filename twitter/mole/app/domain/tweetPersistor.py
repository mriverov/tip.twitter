import logging

from datetime import datetime
from django.utils import timezone

from mole.app.models import Tweet

logger = logging.getLogger(__name__)


class TweetPersistor:
    
    def __init__(self):
        pass

    def save_tweet(self, content, project, user, trend):
        text = content['text']
        retweet_id = None
        if 'retweeted_status' in content and content['retweeted_status'] is not None:
            retweet_id = content['retweeted_status']['id']
        if text is not None:
            text = text.encode('unicode_escape')

        _created_at = content['created_at']
        created_at = None

        if _created_at is not None:
            created_at = _created_at.encode('unicode_escape')
            created_at = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
            timezone.make_aware(created_at, timezone.get_current_timezone())

        tweet = Tweet(tweet_id=content['id'], text=text, retweet_count=content['retweet_count'], author=user,
                      project=project, retweet_id=retweet_id, created_at=created_at, trend=trend)
        tweet.save()
        return tweet
