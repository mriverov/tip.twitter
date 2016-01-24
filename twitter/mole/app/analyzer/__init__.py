from mole.app.analyzer.followers import FollowerAnalyzer
from mole.app.analyzer.hashtag import HashtagAnalyzer
from mole.app.analyzer.url import UrlAnalyzer
from mole.app.models import Project, KeyWord
from pytz import timezone
from datetime import datetime


class MoleConfigurationService:

    def __init__(self):
        self.follower_analyzer = FollowerAnalyzer()
        self.url_analyzer = UrlAnalyzer()
        self.hashtag_analyzer = HashtagAnalyzer()

    def save_project(self, project_name):
        project = Project(name=project_name)
        project.save()
        return project.pk # chequear si esto devuelve el id

    def save_keywords(self, project_id, keywords):

        project = Project.objects.get(pk=project_id)

        for keyword in keywords:
            _keyword = KeyWord(name=keyword, project=project)
            _keyword.save()
        return project

    def start_analyzer(self, project_id, keywords):
        project = self.save_keywords(project_id, keywords)

        date_from = datetime.strptime('2015-12-12', '%Y-%m-%d')
        date_to = datetime.strptime('2015-12-14', '%Y-%m-%d')

        self.follower_analyzer.start_followers_analyzer(date_from, date_to, keywords, project)
        # hay que tener presente que estos analisis se hacen sobre toda la base, no se filtra por proyecto
        self.hashtag_analyzer.start_hashtag_analyzer()
        self.url_analyzer.start_url_analyzer()






