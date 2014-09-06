import logging
from twitter.app.models import TweetUser

#import sys
#sys.path.append('tip.twitter/backend/app')
#from tip.twitter.backend.app.models import *

logger = logging.getLogger()

class UserPersistor:

    def saveUser(self, aName, aDescription):
        _name = None
        _description = None

        if aName is not None:
            _name = aName.encode('unicode_escape')
        if aDescription is not None:
            _description = aDescription.encode('unicode_escape')
        
        user = TweetUser(name = _name, description = _description)
        user.save()
        return user
