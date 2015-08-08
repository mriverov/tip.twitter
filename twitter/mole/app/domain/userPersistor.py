import logging


from mole.app.models import User

logger = logging.getLogger()


class UserPersistor:

    def __init__(self):
        pass

    def save_user(self, user_id, user_content):
        _id = user_id

        if user_content is None:
            user = User(user_id=_id)
            return user.save()

        _screen_name = user_content['screen_name']
        _location = user_content['location']
        _followers_count = user_content['followers_count']

        user = self.validate_and_save(_id, _screen_name, _followers_count, _location)
        return user

    def save_user_with_followers(self, user_content, followers):
        user = self.save_user(user_content)
        user.followers = followers
        user.save()

    def validate_and_save(self, _id, _screen_name, _followers_count,_location ):
        screen_name = None
        location = None

        if _screen_name is not None:
            screen_name = self.encode(_screen_name)
        if _location is not None:
            location = self.encode(_location)

        try:
            user = User.objects.get(user_id=_id)
        except User.DoesNotExist:
            user = User(user_id=_id, screen_name=screen_name, followers_count=_followers_count, location=location)
            user.save()

        return user

    @staticmethod
    def encode(word):
        return word.encode('unicode_escape')
