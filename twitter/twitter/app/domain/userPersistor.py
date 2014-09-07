import logging
from twitter.app.models import TweetUser
from datetime import datetime
from django.utils import timezone

logger = logging.getLogger()

class UserPersistor:

    def saveUser(self, _id, aName, screen_name, aDescription,_followers_count, _friends_count, _statuses_count, 
                 _favourites_count, location, time_zone, created_at):
        _name = None
        _description = None
        _screen_name = None
        _location = None
        _time_zone = None
        _created_at = None

        if aName is not None:
            _name = aName.encode('unicode_escape')
        if aDescription is not None:
            _description = aDescription.encode('unicode_escape')
        if screen_name is not None:
            _screen_name = screen_name.encode('unicode_escape')
        if location is not None:
            _location = location.encode('unicode_escape')
        if time_zone is not None:
            _time_zone = time_zone.encode('unicode_escape')
        if created_at is not None:
            _created_at = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
            timezone.make_aware(_created_at, timezone.get_current_timezone())
        
        user = TweetUser(user_id = _id, name = _name, screen_name= _screen_name, description = _description, followers_count = _followers_count ,
                          friends_count = _friends_count , statuses_count = _statuses_count, favourites_count =_favourites_count, 
                          location = _location, time_zone = _time_zone, created_at=_created_at)
        user.save()
        return user
