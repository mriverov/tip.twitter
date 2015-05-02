import requests
import logging
from mole.app.models import User
from mole.app.domain.userEntityPersistor import UserEntityPersistor

logger = logging.getLogger(__name__)


class FollowerPersistor(UserEntityPersistor):
    
    def __init__(self):
        UserEntityPersistor.__init__(self)

    def process_followers_from(self, user, cursor):
        next_cursor = None
        oauth = self.authenticator.get_oauth()
        api_path = "https://api.twitter.com/1.1/followers/list.json?screen_name=" + user.screen_name + "&count=200"
        if cursor != 0:
            logger.info("Download followers of %s" % user.screen_name)
            url_with_cursor = api_path + "&cursor=" + str(cursor)
            response = requests.get(url=url_with_cursor, auth=oauth)
            response_dictionary = response.json()
            next_cursor = response_dictionary['next_cursor']
            followers = response_dictionary['users']
            self.save_followers(user, followers)
        return next_cursor
    
    def save_followers(self, user, followers):
        for follower_context in followers:
            try:
                follower = User.objects.get(user_id=follower_context['id'])
            except User.DoesNotExist:
                follower = self.save_user_without_followers(follower_context)
            user.followers.add(follower)
        user.save()