from mole.app.analyzer.commons.analyzerDAOService import AnalyzerDAOService
from mole.app.utils import LoggerFactory
from mole.app.analyzer.commons.analyzerService import AnalyzerService
from mole.app.analyzer.commons.filterService import FilterService
from mole.app.models import Project, KeyWord, Tweet

logger = LoggerFactory.create_logger()


class ProjectService:

    def __init__(self):
        self.analyzer_service = AnalyzerService()
        self.filter_service = FilterService()
        self.analyzerDAOService = AnalyzerDAOService()

    def save_project(self, project_name):
        project = Project(name=project_name)
        project.save()
        return project.pk

    def save_keywords(self, project_id, keywords):
        project = Project.objects.get(pk=project_id)

        for keyword in keywords:
            _keyword = KeyWord(name=keyword, project=project)
            _keyword.save()
        return project

    def get_popular_tweets(self, project_id):
        return self.analyzerDAOService.get_popular_tweets(project_id)

    def get_url_user_centrality(self, project_id):
        return self.analyzerDAOService.get_url_user_centrality(project_id)

    def get_trend(self, project_id):
        return self.analyzerDAOService.get_trend(project_id)

    def start(self, project_id, keywords, date_from, date_to):
        logger.info("Starting...")
        project = self.save_keywords(project_id, keywords)

        filters = self.filter_service.generate_filters(keywords, date_from, date_to)
        self.analyzer_service.start_analyzer(project, keywords, filters['hashtags'], filters['urls'], date_from, date_to)
        # hay que tener presente que estos analisis se hacen sobre toda la base, no se filtra por proyecto





