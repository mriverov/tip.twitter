from twitter.app.domain.authenticator import Authenticator
import tweepy

class SearchEngineUser:
    
    def __init__(self):
        autenticator = Authenticator()
        self.auth = autenticator.authenticate()
        
        
    def getUser(self, _id):
        api = tweepy.API(self.auth)
        return api.get_user(_id)