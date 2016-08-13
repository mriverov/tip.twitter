from django.conf.urls import patterns, url, include
from app.views import index, new_project

from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new_project/$', new_project, name='new_project'),
]

# urlpatterns = patterns(url(r'^admin/', include(admin.site.urls)),
#                        url(r'^new_project/$', new_project),
#                        url(r'^start_digger/$', start_digger)) + static(settings.STATIC_URL)
