from mole.app.models import CentralityUrl, CentralityHashtag
from mole.app.utils import LoggerFactory

logger = LoggerFactory.create_logger()


class CentralityPersistor:

    def __init__(self):
        pass

    def persist_url(self, data):
        logger.info("Starting saving centrality")
        for user_id, centrality in data.iteritems():
            url_centrality = CentralityUrl(user_id=user_id, centrality=centrality)
            url_centrality.save()
        logger.info("Finish saving centrality")

    def persist_hashtag(self, data):
        logger.info("Starting saving centrality")
        for user_id, centrality in data.iteritems():
            url_centrality = CentralityHashtag(user_id=user_id, centrality=centrality)
            url_centrality.save()
        logger.info("Finish saving centrality")
