import tweepy

class Digger:

    def __init__(self, auth):
        self.auth = auth
        self.digger = Stream()

    def startStreaming(token, timeout):
        stream = tweepy.streaming.Stream(self.auth, self.digger, timeout)
        print "Streaming started..."	
	    try:
		    stream.filter(track=['obama'])
	    except:
		    print "error!"
		    stream.disconnect()
