from twitter.app.models import Hashtag

class HashtagPersistor:
    
    def saveHashtag(self,hashtag_info, _topic, tweet):
        hashtag = hashtag_info[0]
        if hashtag!=[]:
            if 'text' in hashtag:
                _name = hashtag['text']
                if _name is not None:
                    _name = _name.encode('unicode_escape')
                # TODO
                # count
                hashtag = Hashtag(name = _name, topic = _topic)
                hashtag.save()
                hashtag.tweets.add(tweet)
                hashtag.save()
            
        
    