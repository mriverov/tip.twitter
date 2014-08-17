import tweepy

class UserRepository:
    
    def __init__(self, auth):
        self.auth = auth
        self.repository = tweepy.API(self.auth)

    def getUser(self, userName):
        return self.repository.get_user(userName)
        
