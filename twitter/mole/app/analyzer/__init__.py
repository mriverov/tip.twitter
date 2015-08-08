from mole.app.models import Project
from mole.app.models import KeyWord
from mole.app.domain.tweetPersistor import TweetPersistor
from mole.app.domain.userPersistor import UserPersistor

__author__ = 'Marina'

import pymongo as p

client = p.MongoClient(host='192.168.1.149')
db = client['mole']


class ProjectFactory:
    '''
    Esta clase tiene como objectivo crear un projecto a partir de una configuracion dada
    Entre los parametros estan:
        - from / to : fechas desde y hasta para filtrar los tweets.
        - keywords : palabras clave que identifican un topico o tematica
    '''

    def __init__(self):
        self.tweet_persistor = TweetPersistor()
        self.user_persistor = UserPersistor()

    def save_project(self, project_name, keywords):
        project = Project()
        project.name = project_name
        project = project.save()

        for keyword in keywords:
            _keyword = KeyWord(name=keyword, project=project)
            _keyword.save()
        return project

    def createProject(self, from_date, to_date, keywords, project_name):
        query_date_start = from_date + " 00:01:00 +0000 201"
        query_date_end = to_date + " 23:59:00 +0000 201"

        tweets = db.tweet.find({"created_at": {"$gte": query_date_start, "$lt": query_date_end}})
        # falta filtrar por keywords

        project = self.saveProject(project_name, keywords)

        for tweet in tweets:
            user = self.saveUserModel(tweet)
            self.saveTweetModel(project, tweet, user)

    def saveTweetModel(self, project, content_tweet, user):
        self.tweet_persistor.save_tweet(content_tweet, project, user)

    def saveUserModel(self, tweet):
        followers = tweet['user']['followers']
        followers_to_save = []
        for follower_id in followers:
            user = db.user.find({"id": follower_id})
            followers_to_save.append(self.user_persistor.save_user(user))
        return self.user_persistor.save_user_with_followers(tweet['user'], followers_to_save)
