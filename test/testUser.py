import unittest
import tweepy

class UserTestCase(unittest.TestCase):

    def setUp(self):
        autenticator = Autenticator("API Key", "API Secret", "Access Token", "Access Token Secret")
        auth = autenticator.autenticate()
        self.user = UserRepository(auth)

 def testUser(self):
        othserUser = self.user.getUser('@marley_ok')
        assert othserUser.friends_count>0

    def testFollowing(self):
        othserUser =  self.user.getUser('@EyeOfJackieChan')
        assert not othserUser.following
