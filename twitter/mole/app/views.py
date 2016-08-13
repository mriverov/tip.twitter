from datetime import datetime
import logging

from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from mole.app.analyzer.commons.projectService import ProjectService

logger = logging.getLogger(__name__)
project_service = ProjectService()

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def new_project(request):
    project_name = request.POST['project']
    _keywords = request.POST['tags']

    keywords = _keywords.split(',')

    from_date = datetime.strptime(request.POST['from_date'], '%d/%m/%Y')
    to_date = datetime.strptime(request.POST['to_date'], '%d/%m/%Y')

    project_id = project_service.save_project(project_name)
    project_service.start(project_id, keywords, from_date, to_date)

    logger.info("Create project with name " + project_name + " with id " + str(project_id))
    logger.info("Configured project: " + str(project_id) + " with keywords: " + str(keywords))
    return render_to_response('congratulations.html')



