from __future__ import unicode_literals
import ConfigParser
import tweepy
import requests
from requests_oauthlib import oauth1_auth
from urlparse import parse_qs

import random

keys1 = ['N6iEgbDKY1Bnd5NgPOY0pXgsg','NuNdKNLQ6X5pmTytrM9lEEkv56l0FdW2U3KnS3IwUyBkj70ZPI','2246759519-IOy2xXOaH7Ruy8p8vsAPWeE1gNGWzuqJewMqXlL','Q5tQqAbTebFoSA7aOpVaDoVinm7g2iusHg1FUtQZnHvKQ' ]

#mole-dev-1
keys2 = ['4EGWhOlbKIp8SIXjP56kRdxy8','6j2XJDldCDFNfVM7Urr4Gddu2x1EJVxjSC9dRAdOd1r7KDfu0Z','2463917743-oUidchs8WJT6zEPtp0d6fZCsVCslpyUisthyyem','feLQiY1bR3fOP85ZqNdZyI4h0fdmPJVkAybzbZvTg6408' ]
#mole-dev-2
keys3 = ['xzXAVeTvcNU4dBcE4wnHO0x16','opV46xKmeq0FDD4dOhcEdrdSKL4ps6Tpj9BlioPZTr3TtIEQ6k','2246759519-XGwyYS8VhBdJK0EFsVL40v0jm58kNA54qW83Ccr','CY8MC9VTEi4Di4soPmW80VQhBjegN2NXzOZPgSAO07jeg' ]
#mole-dev-3
keys4 = ['OAd4mP7Z0TXLGL7HvkhvdTA2Z','vXo4B4IQu0DuritJ4p2adnFwLQX6lLO0T8L9SxTsPbZqhT387h','2246759519-DtPqTZdgH4Vxe7V59GZb95ZwHNQYpZeSoN9QeCT','vkWcPMnjoQZgK1X0gLLQzjtn9KMQ4TqPAKfDSozhPZQvY' ]
#mole-dev-4
keys5 = ['ANV6so0pBtDkTx2LX29g1gtj3','Fg5FX6D80avAjzrKEISXMzYRgb7saAz8NPDegzpBpe08HCk0zt','2246759519-BB5UQDbCCn67auDqnVyVSUEKGWgPxKCuIUUQcyD','Lzrz9wMU28FpBhpN9E4iTR75UhJBnCu3x7jIUg2guZ9De']
#mole-dev-5
keys6 = ['vbEjSOwFWth3lNa8D0iX1oguF','1DlX0xG2ofBz8FJH6k9CGSxYS4t67Smq37lWi52k9sHGhHEaKK','2246759519-cOaiwr03EOt58Z6CRjv7OvblWLUW5kKaHPmt9dm','qVESCV61A5B04350rfZfwAONJU3slzlgo3sRfj4hmDEg8']
#mole-dev-6
keys7 = ['YNC95CiQKrEWeSxgJX3hqoWCJ','JyZyM4IWosoT5Gh2fBsc51fNGzjbL3niQKIsVc5vt83ciDCiJl','2246759519-aC6sI1yIXRrQYQSr4uE8LLoMayjz18BpMs6eZHo','TFN1CQq5wjnmjW2IA8lsVid1mIcdtFt83NlWzjw0MJz95' ]

all_keys = [keys1,keys2,keys3,keys4,keys5,keys6,keys7]

class Authenticator:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(['keys.cfg'])
        # self.consumer_key = config.get('API keys', 'apiKey')
        # self.consumer_secret = config.get('API keys', 'apiSecret')
        # self.access_key = config.get('API keys', 'accessToken')
        # self.access_secret = config.get('API keys', 'accessTokenSecret')
	
	keys = random.choice(all_keys)
	
	self.consumer_key = keys[0]
        self.consumer_secret = keys[1]
        self.access_key = keys[2]
        self.access_secret = keys[3]



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
