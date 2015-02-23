import tweepy
import logging
from app.domain.userEntityPersistor import UserEntityPersistor

logger = logging.getLogger()


class UserPersistor(UserEntityPersistor):
    def __init__(self):
        UserEntityPersistor.__init__(self)
        self.auth = self.authenticator.authenticate()
        self.api = tweepy.API(self.auth)

    def get_user_from_api(self, _id):
        api = tweepy.API(self.auth)
        return api.get_user(_id)

    def save_user_from_api(self, user):
        saved_user = self.validate_and_save(user.id, user.name, user.screen_name, user.description,
                                            user.followers_count,
                                            user.friends_count, user.statuses_count,
                                            user.favourites_count,
                                            user.location,
                                            user.time_zone, user.created_at)
        return saved_user

    def save_user(self, user_content):
        user = self.save_user_without_followers(user_content)
        # processFollowers.delay(user=user, cursor=-1)
        # LO SACO DE ACA YA QUE NO ME GUSTA. SE ESTAN CRUZANDO TODAS LAS CAPAS

        return user

    def get_user_mention(self, user_content):
        user = None
        if user_content:
            id_info = user_content[0]
            if id_info != [] and ('id' in id_info):
                _user_mentions = self.get_user_from_api(id_info['id'])
                user = self.get_user_from_api(_user_mentions)
        return user
