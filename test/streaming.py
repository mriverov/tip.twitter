import tweepy

consumer_key = API Key
consumer_secret = API Secret
access_key = Access Token
access_secret = Access Token Secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

l = tweepy.StreamListener()
stream = tweepy.streaming.Stream(auth, l, timeout=60)
stream.filter(track=['barcelona'])
