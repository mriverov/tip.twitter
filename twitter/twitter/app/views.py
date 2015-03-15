import logging
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from app.domain.diggerService import DiggerService

logger = logging.getLogger(__name__)
diggerService = DiggerService()


def get_home(request):
    return render(request, 'home.html')


@csrf_exempt
def new_project(request):
    domain = request.POST['project']
    request.session['domain'] = domain

    logger.info("Create project with name "+domain)
    return render_to_response('configuration.html', {'domain': domain})


@csrf_exempt
def start_digger(request):
    keyword = request.POST['keyword']
    mention = request.POST['mention']
    hashtag = request.POST['hashtag']

    domain = request.session.get('domain')
    diggerService.start_digger_now(domain, keyword, mention, hashtag)

    logger.info(" Configured project with domain "+domain + str(get_message(keyword, mention, hashtag)))
    return render_to_response('streaming_started.html', {'keyword': keyword})


def get_message(keyword, mention, hashtag):
    message = ""
    if keyword is not None:
        message = message+" and keyword "+str(keyword)
    if mention is not None:
        message = message+" and for mention "+str(mention)
    if hashtag is not None:
        message = message+" and hashtag "+str(hashtag)

    return message

