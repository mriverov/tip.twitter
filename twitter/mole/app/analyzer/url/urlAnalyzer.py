from collections import defaultdict

import pymongo as p
from pytz import timezone
from simhash import SimhashIndex, Simhash

from mole.app.analyzer.commons.centrality import Centrality
from mole.app.domain.centralityPersistor import CentralityPersistor
from mole.app.models import Urls, UrlsGraph
from mole.app.utils import LoggerFactory


logger = LoggerFactory.create_logger()
utc = timezone('UTC')

# client = p.MongoClient(host='192.168.1.149')
client = p.MongoClient()
db = client['mole']

f1 = 80
k1 = 8
MIN_URLS_PER_USER = 0

class UrlAnalyzer:

    def __init__(self):
        pass

    def import_urls(self, tweets_urls, project_id):
        for tweet in tweets_urls:
            uid = tweet['user']['id']
            urls = tweet['entities']['urls']
            for an_url in urls:
                url = Urls(user_id=uid, url=an_url['url'], project_id=project_id)
                url.save()

        logger.info("Finished prcessing %s" % len(tweets_urls))

    def process_graph(self, project_id):
        visits = defaultdict(list)
        processed = 0
        urls_db = Urls.objects.filter(project_id=project_id)

        logger.info("Total urls to process "+str(len(urls_db)))
        for url_entry in urls_db:
            visits[url_entry.user_id].append(url_entry.url)
            processed += 1
        logger.info("Urls read")
        logger.info("Urls processed " + str(processed))
        logger.info("Visits count " + str(len(visits)))

        objs = []
        cant_users = 0
        cant_processed = 0
        index = SimhashIndex(objs, f=f1, k=k1)
        for user, urls in visits.iteritems():
            if len(urls) > MIN_URLS_PER_USER:
                simhash = Simhash(urls, f=f1)
                index.add(user, simhash)
                cant_processed += 1
            cant_users += 1
            if cant_users % 10000 == 0:
                logger.info("%s processed" % cant_users)

        logger.info("Simash index build for %i out of %i users" % (cant_processed, len(visits)))
        cant_processed = 0
        for user, urls in visits.iteritems():
            near_dups = index.get_near_dups(Simhash(urls, f=f1))
            for user_near_dups in near_dups:
                user_near_dups = long(user_near_dups)
                if user_near_dups != long(user):
                    urls_near_dups = visits[user_near_dups]
                    intersect = set(urls).intersection(urls_near_dups)
                    ratio = len(intersect)*1.0/len(urls_near_dups)
                    if ratio >= 0.1:
                        url_graph = UrlsGraph(user_oid_i=user, user_oid_j=user_near_dups, ratio=ratio)
                        url_graph.save()
            cant_processed += 1
            if cant_processed % 10000 == 0:
                    logger.info("%i processed" % cant_processed)

    def start_url_analyzer(self, tweets, project_id):
        logger.info("Start importing urls for project "+str(project_id))
        self.import_urls(tweets, project_id)
        logger.info("Finish importing urls")

        logger.info("Start graph")
        self.process_graph(project_id)
        logger.info("Finish graph")

        logger.info("Starting urls centrality")
        centralityUrlCalculator = Centrality()
        persistor = CentralityPersistor()

        urls = UrlsGraph.objects.all()
        centrality = centralityUrlCalculator.calculate_cetrality(urls)
        persistor.persist_url(centrality)
        logger.info("Finish urls centrality")

