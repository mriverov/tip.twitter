from django.conf.urls import url
from app.views import index, new_project, dashboard

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new_project/$', new_project, name='new_project'),
    url(r'^(?P<project_id>[0-9]+)/dashboard/$', dashboard, name='dashboard'),
]

# urlpatterns = patterns(url(r'^admin/', include(admin.site.urls)),
#                        url(r'^new_project/$', new_project),
#                        url(r'^start_digger/$', start_digger)) + static(settings.STATIC_URL)
