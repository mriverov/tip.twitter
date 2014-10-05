from twitter.app.domain.authenticator import Authenticator
import tweepy
from twitter.app.domain.tasks import Scheduler

class SearchEngineUser:
    
    def __init__(self):
        self.autenticator = Authenticator()
        self.auth = self.autenticator.authenticate()
        self.scheduler = Scheduler(self.autenticator)
        
        
    def getUser(self, _id):
        api = tweepy.API(self.auth)
        return api.get_user(_id)

    def startFollowersTask(self, user, user_persistor):
        self.scheduler.processFollowersFrom(user, user_persistor)
        pass