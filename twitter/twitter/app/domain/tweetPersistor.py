#import sys
#sys.path.append('tip.twitter/backend/app')
from twitter.app.models import Tweet


#from tip.twitter.backend.app.models import *

class TweetPersistor:

    def saveTweet(self, atext, _id):
        tweet = Tweet(text= atext, tweetid=_id)
        tweet.save()
        
