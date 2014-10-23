import requests
import logging
from twitter.app.models import User
from twitter.app.domain.userEntityPersistor import UserEntityPersistor

logger = logging.getLogger()

class FollowerPersistor(UserEntityPersistor):
    
    def __init__(self):
        UserEntityPersistor.__init__(self)

    def processFollowersFrom(self, user, cursor):
        next_cursor = None
        oauth = self.autenticator.get_oauth()
        api_path = "https://api.twitter.com/1.1/followers/list.json?screen_name=" + user.screen_name + "&count=200"
        if cursor != 0:
            logger.info("Download followers of %s" %user.screen_name)
            url_with_cursor = api_path + "&cursor=" + str(cursor)
            response = requests.get(url=url_with_cursor, auth=oauth)
            response_dictionary = response.json()
            next_cursor = response_dictionary['next_cursor']
            followers = response_dictionary['users']
            self.saveFollowers(user, followers)
        return next_cursor
    
    def saveFollowers(self, user, followers):
        follower = None
        for follower_context in followers:
            try:
                follower = User.objects.get(user_id = follower_context['id'])
            except User.DoesNotExist:
                follower = self.saveUserWithoutFollowers(follower_context)
            user.followers.add(follower)
        user.save()