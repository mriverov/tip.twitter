import logging
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from mole.app.domain.service import DiggerService, ProjectService, KeyWordService

logger = logging.getLogger(__name__)
diggerService = DiggerService()
project_service = ProjectService()
key_word_service = KeyWordService()


def get_home(request):
    return render(request, 'home.html')


@csrf_exempt
def new_project(request):
    project = request.POST['project']
    request.session['project'] = project

    project_service.save_project(project)

    logger.info("Create project with name " + project)
    return render_to_response('configuration.html', {'project': project})


@csrf_exempt
def start_digger(request):
    _keywords = request.POST['keywords']
    keywords = _keywords.split(',')

    project_name = request.session.get('project')
    project = project_service.get_project(project_name)

    key_word_service.save_keywords(keywords, project)
    diggerService.start_digger_now(keywords, project.id)

    logger.info(" Configured project: " + project_name + " with keywords: " + str(keywords))
    return render_to_response('streaming_started.html', {'keyword': keywords})


