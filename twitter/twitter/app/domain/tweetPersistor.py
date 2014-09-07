#import sys
#sys.path.append('tip.twitter/backend/app')
from twitter.app.models import Tweet


#from tip.twitter.backend.app.models import *

class TweetPersistor:
    #falta retweet_id
    def saveTweet(self, _id, atext, _favorite_count,_retweet_count, user_id):
        _text = None        
        if atext is not None:
            _text = atext.encode('unicode_escape')
        tweet = Tweet(tweetid =_id, text = _text,favorite_count=_favorite_count ,retweet_count=_retweet_count, user = user_id)
        tweet.save()
        
