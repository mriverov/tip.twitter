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

        #self.consumer_key = '4EGWhOlbKIp8SIXjP56kRdxy8'
        #self.consumer_secret = '6j2XJDldCDFNfVM7Urr4Gddu2x1EJVxjSC9dRAdOd1r7KDfu0Z'
        #self.access_key = '2463917743-oUidchs8WJT6zEPtp0d6fZCsVCslpyUisthyyem'
        #self.access_secret = 'feLQiY1bR3fOP85ZqNdZyI4h0fdmPJVkAybzbZvTg6408'
        
    def authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        return auth


    
