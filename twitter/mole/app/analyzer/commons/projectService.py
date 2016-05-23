from mole.app.utils import LoggerFactory
from datetime import datetime

from mole.app.analyzer.commons.analyzerService import AnalyzerService
from mole.app.analyzer.commons.filterService import FilterService
from mole.app.models import Project, KeyWord

logger = LoggerFactory.create_logger()


class ProjectService:

    def __init__(self):
        self.analyzer_service = AnalyzerService()
        self.filter_service = FilterService()

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

    def start(self, project_id, keywords, date_from, date_to):
        logger.info("Starting...")
        project = self.save_keywords(project_id, keywords)

        # date_from = datetime.strptime('2015-12-12', '%Y-%m-%d')
        # date_to = datetime.strptime('2015-12-14', '%Y-%m-%d')

        filters = self.filter_service.generate_filters(keywords, date_from, date_to)
        self.analyzer_service.start_analyzer(project, keywords, filters['hashtags'], filters['urls'], date_from, date_to)
        # hay que tener presente que estos analisis se hacen sobre toda la base, no se filtra por proyecto





