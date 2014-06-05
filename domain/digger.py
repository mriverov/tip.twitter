import tweepy
import authenticator
import stream

class Digger:

    def __init__(self, auth):
        self.auth = auth
        self.digger = stream.Stream()

    def startStreaming(self):
        stream = tweepy.streaming.Stream(self.auth, self.digger)
        print "Streaming started..."
        try:
            stream.filter(track=['obama'])
        except:
            print "error!"
            stream.disconnect()
            
if __name__ == "__main__":
    a = authenticator.Authenticator('4EGWhOlbKIp8SIXjP56kRdxy8', '6j2XJDldCDFNfVM7Urr4Gddu2x1EJVxjSC9dRAdOd1r7KDfu0Z', '2463917743-oUidchs8WJT6zEPtp0d6fZCsVCslpyUisthyyem', 'feLQiY1bR3fOP85ZqNdZyI4h0fdmPJVkAybzbZvTg6408')
    d = Digger(a.authenticate())
    d.startStreaming()
