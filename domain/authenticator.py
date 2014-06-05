import ConfigParser
import tweepy

class Authenticator:

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(['keys.cfg'])
        self.consumer_key = config.get('API keys', 'apiKey')
        self.consumer_secret = config.get('API keys', 'apiSecret')
        self.access_key = config.get('API keys', 'accessToken')
        self.access_secret = config.get('API keys', 'accessTokenSecret')
        
    def authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        return auth


    
