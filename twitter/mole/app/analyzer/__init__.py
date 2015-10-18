from re import match
from mole.app.analyzer.centralityAnalyzer import CentralityAnalyzer
from mole.app.analyzer.trendAnalyzer import TrendAnalyzer

from mole.app.models import Project
from mole.app.models import KeyWord
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

class ProjectFactory:
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

    def save_project(self, project_name, keywords):
        project = Project(name=project_name)
        project.save()

        for keyword in keywords:
            _keyword = KeyWord(name=keyword, project=project)
            _keyword.save()
        return project

    '''
        from_date/to_date : Day Month Day (ex. Wed Jul 05)
    '''
    def create_project(self, from_date, to_date, keywords, project_name):
        logger.info("Starting extracting corpus")
        tweets = db.tweet.find()
        logger.info("Corpus completed!")
        logger.info("Starting saving project")
        project = self.save_project(project_name, keywords)

        logger.info("Starting filter")
        tweets = self.filter_search(from_date, to_date, tweets, keywords)
        logger.info("Filter completed!")

        users_saved = []
        users_by_followers = {}
        tweets_saved = []
        logger.info("Starting saving tweet and user")
        for tweet in tweets:
            user = self.save_user_model(tweet['user'])
            if 'followers' in tweet['user']:
                users_by_followers[user.user_id] = tweet['user']['followers']
            saved_tweet = self.save_tweet_model(project, tweet, user)
            users_saved.append(user)
            tweets_saved.append(saved_tweet)

        self.save_complete_followers(users_saved, users_by_followers)
        logger.info("Tweets and User completed!")

        self.start_analyzer(users_saved, tweets_saved, project)

    def filter_search(self, from_date, to_date, tweets, keywords):
        filtered_tweets = []
        excluded_tweets = []
        matched = False

        for tweet in tweets:
            tweet_date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            # tweet_created_at = utc.localize(tweet_date)
            if to_date > tweet_date > from_date:
                for k in keywords:
                    if k in tweet['text'].lower():
                        matched = True
                        filtered_tweets.append(tweet)
                        break
                if not matched:
                    logger.info("Not matched: "+tweet['text'])
                    excluded_tweets.append(tweet)
            matched = False
        logger.info("Total matched: "+str(len(filtered_tweets)))
        logger.info("Total NOT matched: "+str(len(excluded_tweets)))
        return filtered_tweets

    def start_analyzer(self, users, tweets, project):
        logger.info("Starting centrality calculation")
        self.update_user_centrality(users)
        logger.info("Centrality completed!")
        logger.info("Starting trend analyzer")
        trend_by_tweet = self.trend_analyzer.save_trend(tweets, project)
        self.tweet_persistor.update_trend(trend_by_tweet)
        logger.info("Trend completed!")

    def save_tweet_model(self, project, content_tweet, user):
        return self.tweet_persistor.save_tweet(content_tweet, project, user)

    def save_user_model(self, user_content):
        user = self.user_persistor.save_user(user_content)
        return user

    def save_complete_followers(self, users, users_by_followers):
        not_found = []
        for user_id, followers in users_by_followers.iteritems():
            if followers:
                for follower_id in followers:
                    follower = filter(lambda user: user.user_id == follower_id, users)
                    if not follower:

                        not_found.append(follower_id)
                        self.user_persistor.save_follower(user_id, follower_id, None)
                    else:
                        logger.info("Follower found "+str(follower_id))
                        self.user_persistor.save_follower(user_id, follower_id, follower[0])
        logger.info("Total followers not found "+str(len(not_found)))


    def update_user_centrality(self, users_saved):
        centrality_by_user = self.centrality_analyzer.get_centrality_by_user(users_saved)
        self.user_persistor.update_user_centrality(centrality_by_user)

if __name__ == '__main__':
    date_from = datetime.strptime('2015-01-08', '%Y-%m-%d')
    date_to = datetime.strptime('2015-09-15', '%Y-%m-%d')

    project_factory = ProjectFactory()
    project_factory.create_project(date_from, date_to, ["macri", "massa", "scioli", "elecciones", "corrupcion", "inseguridad", "ganancias"], "politica")