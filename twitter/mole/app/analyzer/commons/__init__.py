from mole.app.models import Project
from mole.app.utils import LoggerFactory
from datetime import datetime
import pymongo as p

logger = LoggerFactory.create_logger()

client = p.MongoClient()
db = client['mole']

class AnalizerService:

    def start_analyzer(self, project_id, keywords, hashtags, urls, from_date, to_date):
        project = Project.objects.get(pk=project_id)
        logger.info("Starting extracting corpus")

        regex = '|'.join(keywords)
        tweets = db.tweet.find({"text": {"$regex": regex, "$options": "i"}},
                               {'entities.hashtags': {"$in": hashtags}},
                               {'entities.urls': {"$in": urls}}).limit(5000)

        # tweets2 = db.stream.find({'text': {'$regex': {"$in": keywords}}},
        #                          {'entities.hashtags': {"$in": hashtags}},
        #                          {'entities.urls': {"$in": urls}}).limit(5000)
        logger.info("Corpus completed! ")

        logger.info("Starting filter")
        tweets = self.filter_search(from_date, to_date, tweets)
        logger.info("Filter completed!")

        for tweet in tweets:
            user = self.save_user_model(tweet['user'])
            saved_tweet = self.save_tweet_model(project, tweet, user)
        logger.info("Users and Tweets completed!")

        self.start_analyzer_hashtag(project_id)
        self.start_analyzer_url(project_id)
        self.start_analyzer_trend(project_id)


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
