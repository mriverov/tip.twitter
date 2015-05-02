import logging

from datetime import datetime
from django.utils import timezone

from mole.app.models import User
from mole.app.domain.authenticator import Authenticator

logger = logging.getLogger()


class UserEntityPersistor:
    def __init__(self):
        self.authenticator = Authenticator()

    def save_user_without_followers(self, user_content):
        _id = user_content['id']
        _name = user_content['name']
        _description = user_content['description']
        _screen_name = user_content['screen_name']
        _location = user_content['location']
        _time_zone = user_content['time_zone']
        _created_at = user_content['created_at']
        _followers_count = user_content['followers_count']
        _friends_count = user_content['friends_count']
        _statuses_count = user_content['statuses_count']
        _favourites_count = user_content['favourites_count']

        created_at0 = None

        if _created_at is not None:
            created_at0 = self.encode(_created_at)
            created_at0 = datetime.strptime(created_at0, '%a %b %d %H:%M:%S +0000 %Y')
            timezone.make_aware(created_at0, timezone.get_current_timezone())

        user = self.validate_and_save(_id, _name, _screen_name, _description, _followers_count, _friends_count,
                                      _statuses_count,
                                      _favourites_count, _location, _time_zone, created_at0)
        return user

    def validate_and_save(self, _id, _name, _screen_name, _description, _followers_count, _friends_count,
                          _statuses_count, _favourites_count, _location, _time_zone, _created_at):
        name0 = None
        description0 = None
        screen_name0 = None
        location0 = None
        time_zone0 = None

        if _name is not None:
            name0 = self.encode(_name)
        if _description is not None:
            description0 = self.encode(_description)
        if _screen_name is not None:
            screen_name0 = self.encode(_screen_name)
        if _location is not None:
            location0 = self.encode(_location)
        if _time_zone is not None:
            time_zone0 = self.encode(_time_zone)

        try:
            user = User.objects.get(user_id=_id)
        except User.DoesNotExist:
            user = User(user_id=_id, name=name0, screen_name=screen_name0, description=description0,
                        followers_count=_followers_count,
                        friends_count=_friends_count, statuses_count=_statuses_count,
                        favourites_count=_favourites_count,
                        location=location0, time_zone=time_zone0, created_at=_created_at)
            user.save()

        return user

    @staticmethod
    def encode(word):
        return word.encode('unicode_escape')
