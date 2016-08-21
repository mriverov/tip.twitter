from mole.app.models import Tweet, CentralityUrl, User, Trend


class CentralityData:
    def __init__(self, name, centrality):
        self.name = name
        self.centrality = centrality

class AnalyzerDAOService:

    def __init__(self):
        pass


    def get_popular_tweets(self, project_id):
        return Tweet.objects.filter(project_id=project_id).order_by('-retweet_count')[0:5]

    def get_url_user_centrality(self, project_id):
        centrality = []

        centrality_url = CentralityUrl.objects.filter(project_id=project_id).order_by('-centrality')[0:5]

        users = [cent.user_id for cent in centrality_url]

        persisted_users = User.objects.filter(user_id__in=users, project_id=project_id)

        for p_user in persisted_users:
            cen = filter(lambda c: c.user_id == p_user.user_id, centrality_url)
            centrality.append(CentralityData(centrality=cen[0].centrality, name=p_user.screen_name))

        return centrality

    def get_trend(self, project_id):
        return Trend.objects.filter(project_id=project_id)





