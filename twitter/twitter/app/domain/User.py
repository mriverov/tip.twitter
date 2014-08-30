import tweepy

class UserRepository:
    
    __init__(self, auth):
        self.auth = auth
        self.repository = tweepy.API(self.auth)

    def getUser(userName):
        return self.repository.get_user(userName)
        
