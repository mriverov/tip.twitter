from twitter.app.models import Topic
from twitter.app.models import Domain

class TopicConfiguration:

    def saveConfiguration(self, dom, topic):
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
        
    def getTopicLikeHashtag(self):
        return "#"+str(self.getTopic())
    
    def getTopicLikeMention(self):
        return "@"+str(self.getTopic())
    
    def getTopicLikeWord(self):
        return str(self.getTopic())
        
    def getTopic(self):
        #por ahora porque solo tenemos uno
        topic = Topic.objects.get()
        return topic.name
    
    

