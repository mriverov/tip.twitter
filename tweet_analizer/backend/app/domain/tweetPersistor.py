from tweet_analizer.app.models import Tweet


class TweetPersistor:

    def saveTweet(self, atext, _id):
        tweet = Tweet(text= atext, tweetid=_id)
        tweet.save()
        
