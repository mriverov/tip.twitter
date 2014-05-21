import unittest
import tweepy

class AutenticationTestCase(unittest.TestCase):
    def setUp(self):
        autenticator = Autenticator("API Key", "API Secret", "Access Token", "Access Token Secret")
        self.auth = autenticator.autenticate()
          
    def testAuth(self):
        assert self.auth.get_username()=="EricaMarinaTIP"        

if __name__ == "__main__":
    unittest.main() # run all tests

