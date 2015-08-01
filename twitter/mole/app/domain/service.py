from mole.app.domain.digger import Digger
from mole.app.models import Project, KeyWord


class DiggerService:
    
    def __init__(self):
        pass

    def start_digger_now(self, keywords, project):
        Digger.start_digger(keywords, project)


class ProjectService:

    def __init__(self):
        pass

    def save_project(self, project_name):
        project = Project()
        project.name = project_name
        project.save()


    def get_project(self, _name):
        return Project.objects.filter(name=_name)[0]


class KeyWordService:

    def __init__(self):
        pass

    def save_keywords(self, keywords, _project):
        for keyword in keywords:
            _keyword = KeyWord(name=keyword, project=_project)
            _keyword.save()
