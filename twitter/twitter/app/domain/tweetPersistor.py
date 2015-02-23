from app.models import Tweet


class TweetPersistor:
    
    def __init__(self):
        pass

    def save_tweet(self, content, _topic, user, user_persistor):
        tweet = self.get_tweet_object(content, _topic, user)
        user_mentions = user_persistor.getUserMention(content['entities']['user_mentions'])
        retweet = self.save_retweet(content, _topic, user_persistor)
        
        tweet.save()
        tweet.retweet = retweet
        if user_mentions is not None:
            tweet.user_mentions.add(user_mentions)
        tweet.save()
        
        return tweet
    
    def save_retweet(self, content, _topic, user_persistor):
        retweet = None
        if 'retweeted_status' in content:
            retweeted_status = content['retweeted_status']
            if retweeted_status is not None:
                retweet_id = retweeted_status['id']
                try:
                    retweet = Tweet.objects.get(tweetid = retweet_id)
                except Tweet.DoesNotExist:
                    user = user_persistor.save_user_without_followers(retweeted_status['user'])
                    retweet = self.get_tweet_object(retweeted_status, _topic, user)
                    retweet.save()
                    retweet.retweet = None
                    user_mention = user_persistor.get_user_mention(retweeted_status['entities']['user_mentions'])
                    if user_mention is not None:
                        retweet.user_mentions.add(user_mention)
                    retweet.save()
        return retweet

    def get_tweet_object(self, content, _topic, _user):
        _id = content['id']
        _favorite_count = content['favorite_count']
        _retweet_count = content['retweet_count']
        _text = content['text'] 
        
        if _text is not None:
            _text = _text.encode('unicode_escape')
        try:
            tweet = Tweet.objects.get(tweetid = _id)
        except Tweet.DoesNotExist:
            tweet = Tweet(tweetid=_id, text=_text, favorite_count=_favorite_count,
                          retweet_count=_retweet_count, author=_user, topic=_topic)
        return tweet

