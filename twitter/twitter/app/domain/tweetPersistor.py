#import sys
#sys.path.append('tip.twitter/backend/app')
from twitter.app.models import Tweet


#from tip.twitter.backend.app.models import *

class TweetPersistor:

    def saveTweet(self, atext, _id, user_id):
        tweet = Tweet(text = atext, tweetid =_id, user = user_id)
        tweet.save()
        
