from collections import defaultdict

import pymongo as p
from pytz import timezone
from simhash import SimhashIndex, Simhash

from mole.app.analyzer.url.centralityByUrl import Centrality
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


def import_urls(tweets_urls):
    for tweet in tweets_urls:
        uid = tweet['user']['id']
        u_url = tweet['entities']['urls'][0]['url']
        url = Urls(user_id=uid, url=u_url)
        url.save()

    logger.info("Finished prcessing %s" % tweets_urls.count())

def process_graph():
    visits = defaultdict(list)
    p = 0;
    for url_entry in Urls.objects.all():
        visits[url_entry.user_id].append(url_entry.url)
        p +=1
    logger.info("Urls read")
    logger.info("Urls processed " + str(p))
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

if __name__ == '__main__':

    logger.info("Start tweet")
    tweets_urls = db.tweet.find({"entities.urls": {'$exists': True, '$not': {'$size': 0}}})
    import_urls(tweets_urls)
    logger.info("Finish tweet")

    logger.info("Start streaming")
    stream_urls = db.stream.find({"entities.urls": {'$exists': True, '$not': {'$size': 0}}})
    import_urls(stream_urls)
    logger.info("Finish streaming")

    logger.info("Start graph")
    process_graph()
    logger.info("Finish graph")

    logger.info("Starting centrality")
    centralityUrlCalculator = Centrality()
    centralityUrlCalculator.calculate_cetrality_by_url()
    logger.info("Finish centrality")
