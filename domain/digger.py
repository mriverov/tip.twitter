import tweepy
import authenticator
import stream
import logging


class Digger:

    

    def __init__(self, auth):
        self.auth = auth
        self.digger = stream.Stream()
        
        self.logger = logging.getLogger("digger")

    def trackingKeys(self):
        return ['#brasil2014','#messi','#wandanara']
    def startStreaming(self):
        stream = tweepy.streaming.Stream(self.auth, self.digger)
        print "Streaming started..."
        try:
            stream.filter(track=self.trackingKeys())
        except Exception as e:
            self.logger.error(e)
            stream.disconnect()
            
if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    a = authenticator.Authenticator()
    d = Digger(a.authenticate())
    d.startStreaming()
