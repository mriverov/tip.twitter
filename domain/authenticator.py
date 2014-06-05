import tweepy

class Authenticator:

    def __init__(self, apiKey, apiSecret, accessToken, accessTokenSecret):
        self.consumer_key = apiKey
        self.consumer_secret = apiSecret
        self.access_key = accessToken
        self.access_secret = accessTokenSecret

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        return auth


    
