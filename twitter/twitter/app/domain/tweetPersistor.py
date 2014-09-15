from twitter.app.models import Tweet

class TweetPersistor:
    
    def saveTweet(self,content, _topic, user, user_persistor):
        _retweet_id = None
        _retweet = None   
        
        _tweet = self.getTweetObject(content, _topic, user)
        _user_mentions = user_persistor.getUserMention(content['entities']['user_mentions'])
        _retweet = self.saveRetweet(content, _topic, user, user_persistor, _retweet_id)
        
        _tweet.save()
        _tweet.retweet = _retweet
        if(_user_mentions is not None):
            _tweet.user_mentions.add(_user_mentions)
        _tweet.save()
        
        return _tweet
    
    def saveRetweet(self, content, _topic, user, user_persistor, _retweet_id):
        _retweet = None
        if 'retweeted_status' in content:
            _retweeted_status = content['retweeted_status']
            if (_retweeted_status is not None):
                _retweet_id = _retweeted_status['id']
                try:
                    _retweet = Tweet.objects.get(tweetid=_retweet_id)
                except Tweet.DoesNotExist:
                    _retweet = self.getTweetObject(_retweeted_status, _topic, user)
                    _retweet.save()
                    _retweet.retweet = None
                    _user_mention = user_persistor.getUserMention(_retweeted_status['entities']['user_mentions'])
                    if _user_mention is not None:
                        _retweet.user_mentions.add(_user_mention)
                    _retweet.save()
        return _retweet

    
    def getTweetObject(self, content, _topic, _user):
        _text = content['text'] 
        _id = content['id']
        _favorite_count = content['favorite_count']
        _retweet_count = content['retweet_count']
        _user = _user
        if _text is not None:
            _text = _text.encode('unicode_escape')
        
        tweet = Tweet(tweetid =_id, text = _text, favorite_count=_favorite_count, 
                  retweet_count=_retweet_count, author = _user, topic = _topic)
        
        return tweet
          
            
        
