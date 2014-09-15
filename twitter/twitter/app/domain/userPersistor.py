import logging
from twitter.app.models import User
from datetime import datetime
from django.utils import timezone
from twitter.app.domain.searchEngineUser import SearchEngineUser

logger = logging.getLogger()

class UserPersistor:

    def saveUser(self, user_content):
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


        if _name is not None:
            _name = _name.encode('unicode_escape')
        if _description is not None:
            _description = _description.encode('unicode_escape')
        if _screen_name is not None:
            _screen_name = _screen_name.encode('unicode_escape')
        if _location is not None:
            _location = _location.encode('unicode_escape')
        if _time_zone is not None:
            _time_zone = _time_zone.encode('unicode_escape')
        if _created_at is not None:
            _created_at = datetime.strptime(_created_at, '%a %b %d %H:%M:%S +0000 %Y')
            timezone.make_aware(_created_at, timezone.get_current_timezone())
        
        user = User(user_id = _id, name = _name, screen_name= _screen_name, description = _description, followers_count = _followers_count ,
                          friends_count = _friends_count , statuses_count = _statuses_count, favourites_count =_favourites_count, 
                          location = _location, time_zone = _time_zone, created_at=_created_at)
        user.save()
        return user
    
    def getUserMention(self, user_content):
        userSearch = SearchEngineUser()
        user = None
        if user_content != []:
            id_info = user_content[0]
            if id_info != []:
                _user_mentions = userSearch.getUser(id_info['id'])
                try:
                    user = User.objects.get(id = _user_mentions.id)
                except User.DoesNotExist:
                    user = self.saveUserFromApi(_user_mentions)        
        return user
    
    def saveUserFromApi(self, user):
        _id = user.id
        _name = user.name
        _description = user.description
        _screen_name = user.screen_name
        _location = user.location
        _time_zone = user.time_zone
        _created_at = user.created_at
        _followers_count = user.followers_count
        _friends_count = user.friends_count
        _statuses_count = user.statuses_count
        _favourites_count = user.favourites_count
        
        if _name is not None:
            _name = _name.encode('unicode_escape')
        if _description is not None:
            _description = _description.encode('unicode_escape')
        if _screen_name is not None:
            _screen_name = _screen_name.encode('unicode_escape')
        if _location is not None:
            _location = _location.encode('unicode_escape')
        if _time_zone is not None:
            _time_zone = _time_zone.encode('unicode_escape')
            
        user = User(user_id = _id, name = _name, screen_name= _screen_name, description = _description, followers_count = _followers_count ,
                          friends_count = _friends_count , statuses_count = _statuses_count, favourites_count =_favourites_count, 
                          location = _location, time_zone = _time_zone, created_at=_created_at)
        user.save()
        return user
        

