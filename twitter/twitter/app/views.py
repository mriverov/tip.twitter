from django.http import HttpResponse
from django.shortcuts import render, render_to_response

from twitter.app.domain.diggerService import DiggerService

diggerService = DiggerService()

def hello(request):
    return HttpResponse("Hello world")


def getHome(request):
    return render(request, 'home.html')


def newProject(request):
    domain = request.POST['project']
    diggerService.startDiggerNow(domain)

    return render_to_response('configuration.html', {'domain':domain})