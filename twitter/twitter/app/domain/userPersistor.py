import tweepy
import logging

from twitter.app.domain.tasks import processFollowers
from twitter.app.domain.userEntityPersistor import UserEntityPersistor

logger = logging.getLogger()

class UserPersistor(UserEntityPersistor):
    
    def __init__(self):
        UserEntityPersistor.__init__(self)
        self.auth = self.autenticator.authenticate()
        self.api = tweepy.API(self.auth)
        
    def getUserFromApi(self, _id):
        api = tweepy.API(self.auth)
        return api.get_user(_id)

    def saveUserFromApi(self, user):
        saved_user = self.validateAndSave(user.id, user.name, user.screen_name, user.description, user.followers_count,
                                          user.friends_count, user.statuses_count, user.favourites_count, user.location,
                                          user.time_zone, user.created_at)
        return saved_user
    
    def saveUser(self, user_content):
        user = self.saveUserWithoutFollowers(user_content)
        processFollowers.delay(user=user, cursor=-1)
        
        return user
    
    def getUserMention(self, user_content):
        user = None
        if user_content != []:
            id_info = user_content[0]
            if id_info != [] and ('id' in id_info):
                _user_mentions = self.getUserFromApi(id_info['id'])
                user = self.saveUserFromApi(_user_mentions)        
        return user
            
