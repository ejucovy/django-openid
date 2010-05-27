from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
from auth_user_provider import AuthProvider, openid_page

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', lambda r: HttpResponseRedirect('/openid/')),
                       (r'^server/$', AuthProvider()),
                       (r'^accounts/', include('django.contrib.auth.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       url(r'^(\w+)/$', openid_page,
                           name='openid_page'),
)
