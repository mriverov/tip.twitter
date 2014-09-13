#import sys
#sys.path.append('tip.twitter/backend/app')
from twitter.app.models import Tweet


#from tip.twitter.backend.app.models import *

class TweetPersistor:
    #falta retweet_id
    def saveTweet(self, _id, atext, _favorite_count,_retweet_count, _user, _retweet, _topic):
        _text = None        
        if atext is not None:
            _text = atext.encode('unicode_escape')
        tweet = Tweet(tweetid =_id, text = _text,favorite_count=_favorite_count,
                      retweet_count=_retweet_count, author = _user, retweet = _retweet,
                      topic = _topic)
        tweet.save()
        
