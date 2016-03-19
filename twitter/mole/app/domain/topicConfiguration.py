from app.models import Domain, Topic


# Deprecated
class TopicConfiguration:

    def __init__(self):
        pass

    @staticmethod
    def save_configuration(dom, topic, mention, hashtag):
        try:
            _domain = Domain.objects.get(name=dom)
        except Domain.DoesNotExist:
            _domain = Domain(name=dom)
            _domain.save()
        
        try:
            Topic.objects.get(name=topic)
        except Topic.DoesNotExist:
            _topic = Topic(name=topic, domain=_domain)
            _topic.save()

        try:
            Topic.objects.get(name=mention)
        except Topic.DoesNotExist:
            _topic = Topic(name=mention, domain=_domain)
            _topic.save()

        try:
            Topic.objects.get(name=hashtag)
        except Topic.DoesNotExist:
            _topic = Topic(name=hashtag, domain=_domain)
            _topic.save()