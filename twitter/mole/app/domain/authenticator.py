from __future__ import unicode_literals
import ConfigParser
import tweepy
import requests
from requests_oauthlib import oauth1_auth
from urlparse import parse_qs


class Authenticator:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(['keys.cfg'])
        # self.consumer_key = config.get('API keys', 'apiKey')
        # self.consumer_secret = config.get('API keys', 'apiSecret')
        # self.access_key = config.get('API keys', 'accessToken')
        # self.access_secret = config.get('API keys', 'accessTokenSecret')

        self.consumer_key = '4EGWhOlbKIp8SIXjP56kRdxy8'
        self.consumer_secret = '6j2XJDldCDFNfVM7Urr4Gddu2x1EJVxjSC9dRAdOd1r7KDfu0Z'
        self.access_key = '2463917743-oUidchs8WJT6zEPtp0d6fZCsVCslpyUisthyyem'
        self.access_secret = 'feLQiY1bR3fOP85ZqNdZyI4h0fdmPJVkAybzbZvTg6408'

        self.request_token_url = "https://api.twitter.com/oauth/request_token"
        self.authorize_url = "https://api.twitter.com/oauth/authorize?self.access_key="
        self.access_token_url = "https://api.twitter.com/oauth/access_token"

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        return auth

    def setup_oauth(self):
        """Authorize your app via identifier."""
        # Request token
        oauth = oauth1_auth.OAuth1(self.consumer_key, client_secret=self.consumer_secret)
        r = requests.post(url=self.request_token_url, auth=oauth)
        credentials = parse_qs(r.content)

        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]

        # Authorize
        self.authorize_url = self.authorize_url + resource_owner_key
        print 'Please go here and authorize: ' + self.authorize_url

        verifier = raw_input('Please input the verifier: ')
        oauth = oauth1_auth.OAuth1(self.consumer_key,
                                   client_secret=self.consumer_secret,
                                   resource_owner_key=resource_owner_key,
                                   resource_owner_secret=resource_owner_secret,
                                   verifier=verifier)

        # Finally, Obtain the Access Token
        r = requests.post(url=self.access_token_url, auth=oauth)
        credentials = parse_qs(r.content)
        token = credentials.get('self.access_key')[0]
        secret = credentials.get('self.access_secret')[0]

        return token, secret

    def get_oauth(self):
        # self.setup_oauth()
        oauth = oauth1_auth.OAuth1(self.consumer_key,
                                   client_secret=self.consumer_secret,
                                   resource_owner_key=self.access_key,
                                   resource_owner_secret=self.access_secret)
        return oauth