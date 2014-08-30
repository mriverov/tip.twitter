import tweepy
import authenticator
import stream

class Digger:

    

    def __init__(self, auth):
        self.auth = auth
        self.digger = stream.Stream()

    def trackingKeys(self):
        return ['#obama']

    def startStreaming(self):
        stream = tweepy.streaming.Stream(self.auth, self.digger)
        print "Streaming started..."
        try:
            stream.filter(track=self.trackingKeys())
        except Exception as e:
            print e
            stream.disconnect()

            
if __name__ == "__main__":
    a = authenticator.Authenticator()
    d = Digger(a.authenticate())
    d.startStreaming()
