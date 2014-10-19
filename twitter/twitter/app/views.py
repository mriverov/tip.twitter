from django.http import HttpResponse
from django.shortcuts import render, render_to_response
#from django.core.context_processors import csrf

def hello(request):
    return HttpResponse("Hello world")


def getHome(request):
    return render(request, 'home.html')


def newProject(request):
    domain = request.POST['project']
      

    return render_to_response('configuration.html', {'domain':domain})