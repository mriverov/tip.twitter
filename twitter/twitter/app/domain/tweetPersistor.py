#import sys
#sys.path.append('tip.twitter/backend/app')
from twitter.app.models import Tweet


#from tip.twitter.backend.app.models import *

class TweetPersistor:

    def saveTweet(self, atext, _id, user_id):
        _text = None        
        if atext is not None:
            _text = atext.encode('unicode_escape')
        tweet = Tweet(text = _text, tweetid =_id, user = user_id)
        tweet.save()
        
