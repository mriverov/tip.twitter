from collections import defaultdict

import django
import pymongo as p
from pytz import timezone
from simhash import SimhashIndex, Simhash

from mole.app.analyzer.commons.centrality import Centrality
from mole.app.domain.centralityPersistor import CentralityPersistor
from mole.app.models import Hashtag, HashtagGraph
from mole.app.utils import LoggerFactory

logger = LoggerFactory.create_logger()
utc = timezone('UTC')

client = p.MongoClient()
db = client['mole']

f1 = 80
k1 = 8
MIN_HASHTAG_PER_USER = 2

class HashtagAnalyzer:

    def __init__(self):
        pass

    def import_hashtags(self, tweets_hashtags, project_id):
        not_process = 0
        for tweet in tweets_hashtags:
            uid = tweet['user']['id']
            hashtags = tweet['entities']['hashtags']
            for a_hashtag in hashtags:
                hashtag = Hashtag(user_id=uid, hashtag=a_hashtag['text'], project_id=project_id)
                try:
                    hashtag.save()
                except django.db.utils.OperationalError as e:
                    logger.error("Could not process hashtag for user %s" % str(uid))
                    not_process += 1
        logger.info("Finished processing %s" % len(tweets_hashtags))
        logger.info("Hashtags rejected %s" % not_process)

    def process_graph(self, project_id):
        visits = defaultdict(list)
        p = 0;
        hashtagsDb = Hashtag.objects.filter(project_id=project_id)

        logger.info("Total hashtags to process "+str(len(hashtagsDb)))

        for hashtag_entry in hashtagsDb:
            visits[hashtag_entry.user_id].append(hashtag_entry.hashtag)
            p +=1

        logger.info("Hashtag read")
        logger.info("Hashtag processed " + str(p))
        logger.info("Visits count " + str(len(visits)))

        objs = []
        cant_users = 0
        cant_processed = 0
        index = SimhashIndex(objs, f=f1, k=k1)
        for user, hashtags in visits.iteritems():
            if len(hashtags) > MIN_HASHTAG_PER_USER:
                simhash = Simhash(hashtags, f=f1)
                index.add(user, simhash)
                cant_processed += 1
            cant_users += 1
            if cant_users % 10000 == 0:
                logger.info("%s processed" % cant_users)

        logger.info("Simash index build for %i out of %i users" % (cant_processed, len(visits)))
        cant_processed = 0
        for user, hashtags in visits.iteritems():
            near_dups = index.get_near_dups(Simhash(hashtags, f=f1))
            for user_near_dups in near_dups:
                user_near_dups = long(user_near_dups)
                if user_near_dups != long(user):
                    hashtag_near_dups = visits[user_near_dups]
                    intersect = set(hashtags).intersection(hashtag_near_dups)
                    ratio = len(intersect)*1.0/len(hashtag_near_dups)
                    if ratio >= 0.1:
                        hashtag_graph = HashtagGraph(user_oid_i=user, user_oid_j=user_near_dups, ratio=ratio)
                        hashtag_graph.save()
            cant_processed += 1
            if cant_processed % 10000 == 0:
                    logger.info("%i processed" % cant_processed)

    def start_hashtag_analyzer(self, tweets, project_id):

        logger.info("Read tweets from django for project " + str(project_id))
        self.import_hashtags(tweets, project_id)
        logger.info("Finish reading tweets")


        logger.info("Start graph")
        self.process_graph(project_id)
        logger.info("Finish graph")

        logger.info("Starting centrality")
        centralityCalculator = Centrality()
        persistor = CentralityPersistor()

        hashtags = HashtagGraph.objects.all()
        centrality = centralityCalculator.calculate_cetrality(hashtags)
        persistor.persist_hashtag(centrality)
        logger.info("Finish centrality")
