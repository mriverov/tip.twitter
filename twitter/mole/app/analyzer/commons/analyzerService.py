from mole.app.analyzer.hashtag.hashtagAnalyzer import HashtagAnalyzer
from mole.app.analyzer.trend.trendAnalyzer import TrendAnalyzer
from mole.app.analyzer.url.urlAnalyzer import UrlAnalyzer
from mole.app.utils import LoggerFactory
from datetime import datetime
import pymongo as p


logger = LoggerFactory.create_logger()

client = p.MongoClient()
db = client['mole']

class AnalizerService:

    def __init__(self):
        self.url_analyzer = UrlAnalyzer()
        self.hashtag_analyzer = HashtagAnalyzer()
        self.trend_analyzer = TrendAnalyzer()


    def start_analyzer(self, project, keywords, hashtags, urls, from_date, to_date):
        logger.info("Starting extracting corpus")

        regex = '|'.join(keywords)
        tweets = db.tweet.find({"text": {"$regex": regex, "$options": "i"}},
                               {'entities.hashtags': {"$in": hashtags}},
                               {'entities.urls': {"$in": urls}})

        # tweets2 = db.stream.find({'text': {'$regex': {"$in": keywords}}},
        #                          {'entities.hashtags': {"$in": hashtags}},
        #                          {'entities.urls': {"$in": urls}}).limit(5000)
        logger.info("Corpus completed! "+ str(len(tweets)))

        logger.info("Starting filter")
        tweets = self.filter_search(from_date, to_date, tweets)
        logger.info("Filter completed!")

        logger.info("Start saving tweets " + str(len(tweets)))

        for tweet in tweets:
            user = self.save_user_model(tweet['user'])
            self.save_tweet_model(project, tweet, user)
        logger.info("Users and Tweets completed!")

        self.hashtag_analyzer.start_hashtag_analyzer(tweets)
        self.url_analyzer.start_url_analyzer(tweets)
        self.trend_analyzer.build_trend(project)


    def filter_search(self, from_date, to_date, tweets):
        filtered_tweets = []
        excluded_tweets = 0
        matched = False

        for tweet in tweets:
            tweet_date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            if to_date > tweet_date > from_date:
                matched = True
                filtered_tweets.append(tweet)
            if not matched:
                excluded_tweets += 1
            matched = False
        logger.info("Total matched: " + str(len(filtered_tweets)))
        logger.info("Total NOT matched: " + str(excluded_tweets))
        return filtered_tweets