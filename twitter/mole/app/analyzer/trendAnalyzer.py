from mole.app.models import Trend

__author__ = 'Marina'

from pytz import timezone
from datetime import datetime
from itertools import groupby

utc = timezone('UTC')


class TweetByTime:
    def __init__(self, year, month, day, hour, minute, tweet):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.tweet = tweet


class TrendAnalyzer:
    def __init__(self):
        pass

    """
        Como primer paso se crea un objeto nuevo que contiene el tweet y la hora en la que fue creado, de tal forma
        que se pueda manipular esa fecha para agrupar por mes, dia y hora.
        Como segunda instancia, se aplica un algoritmo de agrupamiento, el primer nivel es por mes. Eso nos retorna una lista de listas,
        luego se toma cada lista y se aplica el mismo algoritmo pero agurpado por dia y asi sucesivamente hasta hacerlo por hora.
        Como ultimo paso se arma el objeto Trend, donde ya tenemos el set de tweets creados en el periodo minimo de tiempo (1 hora)
        y luego se retorna un diccionario con la referencia al tweet para poder asociarlo en le modelo de django.
    """
    def save_trend(self, tweets, project):
        tweets_by_time = []
        # crea objetos TweetByTime con la fecha mejor expresada
        for tweet in tweets:
            created_at = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            tweet_created_at = utc.localize(created_at)
            tweet_by_time = TweetByTime(tweet_created_at.year, tweet_created_at.month,
                                        tweet_created_at.day, tweet_created_at.hour, tweet_created_at.minute, tweet)
            tweets_by_time.append(tweet_by_time)

        # retorna una lista de listas agrupadas por mes
        tweet_group_by_month = []
        for key, group in groupby(tweets_by_time, lambda x: x.month):
            by_month = [t for t in group]
            tweet_group_by_month.append(by_month)

        # retorna una lista de listas agrupadas por dia
        tweet_group_by_day = []
        for tweet_month in tweet_group_by_month:
            for key, group in groupby(tweet_month, lambda x: x.day):
                by_day = [t for t in group]
                tweet_group_by_day.append(by_day)

        # retorna una lista de listas agrupadas por hora
        tweet_group_by_hour = []
        for tweet_day in tweet_group_by_day:
            for key, group in groupby(tweet_day, lambda x: x.hour):
                by_hour = [t for t in group]
                tweet_group_by_hour.append(by_hour)

        # save Trend
        trend_by_tweet = {}
        for tweet_hour in tweet_group_by_hour:
            trend = Trend(date=tweet_hour.tweet.created_at, tweets_count=len(tweet_hour), project=project)
            trend.save()
            for tweet in tweet_hour:
                trend_by_tweet[tweet.tweet_id] = trend

        return trend_by_tweet
