from django.conf.urls import patterns, url, include
from app.views import get_home, new_project, start_digger

from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(''
                       , url(r'^home/$', get_home),
                       url(r'^admin/', include(admin.site.urls)), 
                       url(r'^new_project/$', new_project),
                       url(r'^start_digger/$', start_digger), ) + static(settings.STATIC_URL, 
                       
)
