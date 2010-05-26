from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
from anon_provider import AnonProvider, openid_page

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', lambda r: HttpResponseRedirect('/openid/')),
                       (r'^server/$', AnonProvider()),
                       (r'^accounts/', include('django.contrib.auth.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       url(r'^(\w+)/$', openid_page,
                           name='openid_page'),
)
