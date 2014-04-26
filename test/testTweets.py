import tweepy

consumer_key = API Key
consumer_secret = API Secret
access_key = Access Token
access_secret = Access Token Secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
user = api.get_user('@marley_ok')

print user.screen_name
print user.followers_count
#esto no lo probe porque debe de tener un millon de amigos :P
#for friend in user.friends():
   #print friend.screen_name
