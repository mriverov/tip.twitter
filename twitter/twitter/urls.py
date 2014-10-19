from django.conf.urls import patterns, url
from app.views import getHome, newProject

from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()



urlpatterns = patterns('',
    url(r'^home/$', getHome),
    url(r'^new_project/$', newProject),
       
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
