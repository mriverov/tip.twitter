import tweepy

class Stream(tweepy.StreamListener):

    def on_data(self, data):
		print data
		return True
	
    def on_error(self, status):
		print status
