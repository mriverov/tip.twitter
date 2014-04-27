import unittest
import tweepy

class AutenticationTestCase(unittest.TestCase):
    def setUp(self):
        self.consumer_key = "API Key"
        self.consumer_secret = "API Secret"
        self.access_key = "Access Token"
        self.access_secret = "Access Token Secret"
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
    
    def testAuth(self):
        assert self.auth.get_username()=="EricaMarinaTIP"

    def testUser(self):
        api = tweepy.API(self.auth)
        user = api.get_user('@marley_ok')
        assert user.friends_count>0

    def testFollowing(self):
        api = tweepy.API(self.auth)
        user = api.get_user('@EyeOfJackieChan')
        assert not user.following
        

if __name__ == "__main__":
    unittest.main() # run all tests

