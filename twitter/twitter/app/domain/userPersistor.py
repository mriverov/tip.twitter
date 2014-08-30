import logging
from twitter.app.models import TweetUser

#import sys
#sys.path.append('tip.twitter/backend/app')
#from tip.twitter.backend.app.models import *

logger = logging.getLogger()

class UserPersistor:

    def saveUser(self, aName, aDescription):
        user = TweetUser(name= aName, description=aDescription)
        user.save()
        
