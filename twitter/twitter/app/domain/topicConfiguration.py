from app.models import Domain, Topic


class TopicConfiguration:

    def __init__(self):
        pass

    def save_configuration(self, dom, topic):
        try:
            Domain.objects.get(name=dom)
        except Domain.DoesNotExist:
            _domain = Domain(name=dom)
            _domain.save()
        
        try:
            Topic.objects.get(name=topic)
        except Topic.DoesNotExist:
            _topic = Topic(name=topic, domain=_domain)
            _topic.save() 
        
    def get_topic_like_hashtag(self):
        return "#"+str(self.getTopic())
    
    def get_topic_like_mention(self):
        return "@"+str(self.getTopic())
    
    def get_topic_like_word(self):
        return str(self.getTopic())
        
    def get_topic(self):
        # por ahora porque solo tenemos uno
        topic = Topic.objects.get()
        return topic.name
    
    

