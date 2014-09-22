from twitter.app.domain.authenticator import Authenticator
import tweepy
import requests

class SearchEngineUser:
    
    def __init__(self):
        self.autenticator = Authenticator()
        self.auth = self.autenticator.authenticate()
        
        
    def getUser(self, _id):
        api = tweepy.API(self.auth)
        return api.get_user(_id)
    
    
    def processFollowersFrom(self, id_user, user_screen_name, user_persistor):
        oauth = self.autenticator.get_oauth()
        cursor = -1
        api_path = "https://api.twitter.com/1.1/followers/ids.json?screen_name="+user_screen_name
        url_with_cursor = api_path + "&cursor=" + str(cursor)
        response_dictionary = requests.get(url=url_with_cursor, auth=oauth)
        while cursor!=0:
            cursor = response_dictionary['next_cursor']
            followers_ids = response_dictionary['ids']
            user_persistor.saveFollowersFrom(id_user, followers_ids)
            
        