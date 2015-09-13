__author__ = 'Marina'

import networkx as nx
import pymongo as p
import mole.app.utils

# import matplotlib.pyplot as plt

client = p.MongoClient()
db = client['mole']

class Trend:
    def __init__(self, _date, _start, _end, _tweets):
        self.date = _date
        self.start_range = _start
        self.end_range = _end
        self.tweets_id = _tweets
        self.count = len(_tweets)

class TrendFactory:
    '''
    Crea un objeto tendencia para una fecha en particular y un topico dado.
    '''
    def loadTendences(self, date, topic=None):
        for i in range(0, 24):
            query_date_start = date + " " + str(i).zfill(2) + ":01:00 +0000 201"
            query_date_end = date + " " + str(i).zfill(2) + ":59:00 +0000 201"
            print(query_date_start)
            print(query_date_end)
            tweets = db.tweet.find({ "created_at" : { "$gte" : query_date_start, "$lt": query_date_end }})
            tweets_id = []
            for tweet in tweets:
                tweets_id.append(tweet['id'])
            tendence = Tendence(date, i, i + 1, tweets_id)
            db.tendence.save(tendence.__dict__)



