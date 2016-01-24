import logging
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from mole.app.analyzer import MoleConfigurationService

logger = logging.getLogger(__name__)
mole_configuration = MoleConfigurationService()


def get_home(request):
    return render(request, 'home.html')


@csrf_exempt
def new_project(request):
    project = request.POST['project']
    request.session['project'] = project

    project_id = mole_configuration.save_project(project)

    logger.info("Create project with name " + project + " with id " + project_id)
    return render_to_response('configuration.html', {'project': project_id})


@csrf_exempt
def start_digger(request):
    _keywords = request.POST['keywords']
    keywords = _keywords.split(',')

    project_id = request.session.get('project')

    mole_configuration.start_analyzer(project_id, keywords)

    logger.info(" Configured project: " + project_id + " with keywords: " + str(keywords))
    return render_to_response('streaming_started.html', {'keyword': keywords})


