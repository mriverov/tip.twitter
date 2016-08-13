import tweepy

consumer_key = "API Key"
consumer_secret = "API Secret"
access_key = "Access Token"
access_secret = "Access Token Secret"

class StdOutListener(tweepy.StreamListener):
	""" A listener handles tweets are the received from the stream.
   This is a basic listener that just prints received tweets to stdout.
   """
	def on_data(self, data):
		print "New data received" 
		print data
		return True
	
	def on_error(self, status):
		print status


if __name__ == '__main__':
	print "Authorizing with twitther oauth" 

	l = StdOutListener()
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	stream = tweepy.streaming.Stream(auth, l, timeout= 10)
	print "Streaming started..."	
	try:
		stream.filter(track=['icardi'])
	except:
		print "error!"
		stream.disconnect()

