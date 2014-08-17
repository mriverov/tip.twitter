import logging
from tweet_analizer.app.models import TweetUser


logger = logging.getLogger()

class UserPersistor:

    def saveUser(self, aName, aDescription):
        user = TweetUser(name= aName, description=aDescription)
        user.save()
        
