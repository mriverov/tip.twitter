import logging


from mole.app.models import User

logger = logging.getLogger()


class UserPersistor:

    def __init__(self):
        pass

    def save_follower(self, user, follower_id):
        '''
        try:
            follower = User.objects.get(user_id=follower_id)
        except User.DoesNotExist:
            follower = User(user_id=follower_id)
            follower.save()

        user.followers.add(follower)
        user.save()
        # user.add_relationship(follower)
        return user
        '''
        try:
            follower = User.objects.get(user_id=follower_id)
        except User.DoesNotExist:
            follower = User(user_id=follower_id)
            follower.save()
        return follower


    def save_user(self, user_content):
        _user_id = user_content['id']
        _screen_name = user_content['screen_name']
        _location = user_content['location']
        _followers_count = user_content['followers_count']

        user = self.validate_and_save(_user_id, _screen_name, _followers_count, _location)
        return user

    def validate_and_save(self, _id, _screen_name, _followers_count, _location):
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

    def update_user_centrality(self, centrality_dic):
        for user_id, centrality in centrality_dic.iteritems():
            User.objects.filter(user_id=user_id).update(centrality=centrality)

    @staticmethod
    def encode(word):
        return word.encode('unicode_escape')
