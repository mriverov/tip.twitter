from mole.app.analyzer.followers.centralityAnalyzer import CentralityAnalyzer
from mole.app.analyzer.trend.trendAnalyzer import TrendAnalyzer
from mole.app.domain.tweetPersistor import TweetPersistor
from mole.app.domain.userPersistor import UserPersistor
from mole.app.utils import LoggerFactory
from pytz import timezone
from datetime import datetime

__author__ = 'Marina'

import pymongo as p

logger = LoggerFactory.create_logger()
utc = timezone('UTC')

# client = p.MongoClient(host='192.168.1.149')
client = p.MongoClient()
db = client['mole']

class FollowerAnalyzer:
    """
        Esta clase tiene como objectivo crear un projecto a partir de una configuracion dada
        Entre los parametros estan:
            - from / to : fechas desde y hasta para filtrar los tweets.
            - keywords : palabras clave que identifican un topico o tematica
    """

    def __init__(self):
        self.tweet_persistor = TweetPersistor()
        self.user_persistor = UserPersistor()
        self.centrality_analyzer = CentralityAnalyzer()
        self.trend_analyzer = TrendAnalyzer()


    '''
        from_date/to_date : Day Month Day (ex. Wed Jul 05)
    '''
    def start_followers_analyzer(self, from_date, to_date, keywords, project):
        logger.info("Starting extracting corpus")
        tweets = db.tweet.find()
        #tweets = db.tweet.find({'text': {'$regex': {"$in": keywords}}}, {'bla.hashtag' : hashtags}, {'bla.url' : urls}).limit(5000)
        logger.info("Corpus completed! ")

        logger.info("Starting filter")
        tweets = self.filter_search(from_date, to_date, tweets)
        logger.info("Filter completed!")

        # sacar esto a un archivo para mejorar performance
        users_saved = {}
        tweets_saved = []
        logger.info("Starting saving tweet and user")
        for tweet in tweets:
            user = self.save_user_model(tweet['user'])
            if 'followers' in tweet['user']:
                user = self.save_complete_followers(user, tweet['user']['followers'], users_saved)
            saved_tweet = self.save_tweet_model(project, tweet, user)
            tweets_saved.append(saved_tweet)
            users_saved[user.user_id]=user
        logger.info("Users and Tweets completed!")

        self.start_analyzer(users_saved.values(), tweets_saved, project)

    def filter_search(self, from_date, to_date, tweets):
        filtered_tweets = []
        excluded_tweets = 0
        matched = False

        for tweet in tweets:
            tweet_date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            # tweet_created_at = utc.localize(tweet_date)
            # logger.info(tweet_date)
            if to_date > tweet_date > from_date:
                # for k in keywords:
                # if k in tweet['text'].lower():
                matched = True
                filtered_tweets.append(tweet)
                #        break
            if not matched:
                #logger.info("Not matched: "+tweet['text'])
                excluded_tweets += 1
            matched = False
        logger.info("Total matched: "+str(len(filtered_tweets)))
        logger.info("Total NOT matched: "+str(excluded_tweets))
        return filtered_tweets

    def start_analyzer(self, users, tweets, project):
        logger.info("Starting centrality calculation")
        self.update_user_centrality(users)
        logger.info("Centrality completed!")
        logger.info("Starting trend followersAnalyzer")
        trend_by_tweet = self.trend_analyzer.save_trend(tweets, project)
        self.tweet_persistor.update_trend(trend_by_tweet)
        logger.info("Trend completed!")

    def save_tweet_model(self, project, content_tweet, user):
        return self.tweet_persistor.save_tweet(content_tweet, project, user)

    def save_user_model(self, user_content):
        user = self.user_persistor.save_user(user_content)
        return user

    def save_complete_followers(self, user, follower_ids, users_saved):
        followers = []
        if not follower_ids:
            return user
        for follower_id in follower_ids:
            follower = users_saved.get(follower_id, None)
            if follower is None:
                follower = self.user_persistor.save_follower(follower_id)
            followers.append(follower)
        user.followers.add(*followers)
        user.save()
        logger.info("Finishing saving followers: " + str(len(follower_ids)))
        return user


    def update_user_centrality(self, users_saved):
        centrality_by_user = self.centrality_analyzer.get_centrality_by_user(users_saved)
        self.user_persistor.update_user_centrality(centrality_by_user)


'''
if __name__ == '__main__':
    date_from = datetime.strptime('2015-12-12', '%Y-%m-%d')
    date_to = datetime.strptime('2015-12-14', '%Y-%m-%d')

    project_factory = ProjectFactory()
    project_factory.create_project(date_from, date_to, ["macri", "massa", "scioli", "elecciones", "corrupcion",

                                                        "inseguridad", "ganancias"], "politica")
'''