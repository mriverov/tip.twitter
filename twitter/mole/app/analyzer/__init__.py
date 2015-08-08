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
        project = Project(name=project_name)
        project.save()

        for keyword in keywords:
            _keyword = KeyWord(name=keyword, project=project)
            _keyword.save()
        return project

    '''
        from_date/to_date : Day Month Day (ex. Wed Jul 05)
    '''
    def createProject(self, from_date, to_date, keywords, project_name):
        query_date_start = from_date + " 00:01:00 +0000 2015"
        query_date_end = to_date + " 23:59:00 +0000 2015"

        tweets = db.tweet.find({"created_at": {"$gte": query_date_start, "$lt": query_date_end},
                                'text': {'$regex': {"$in": keywords}}})
        project = self.save_project(project_name, keywords)

        for tweet in tweets:
            user = self.saveUserModel(tweet['user'])
            self.saveTweetModel(project, tweet, user)

    def saveTweetModel(self, project, content_tweet, user):
        self.tweet_persistor.save_tweet(content_tweet, project, user)

    def saveUserModel(self, user_content):
        followers_to_save = []
        if 'followers' in user_content:
            followers = user_content['followers']
            if followers:
                for follower_id in followers:
                    follower = db.user.find({"id": follower_id})
                    if follower.count() == 0:
                        follower = None
                    else:
                        follower = follower.next()
                    saved_follower = self.user_persistor.save_user(follower_id, follower)
                    followers_to_save.append(saved_follower)
        return self.user_persistor.save_user_with_followers(user_content, followers_to_save)

if __name__ == '__main__':
    project_factory = ProjectFactory()
    project_factory.createProject("Mon Aug 03", "Sat Aug 08", ["macri", "massa", "scioli", "elecciones", "corrupcion", "inseguridad", "ganancias"], "politica")