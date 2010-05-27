from django_openid.provider import Provider
from django.shortcuts import render_to_response as render

from django.core.urlresolvers import reverse

from webob import Request

class AuthProvider(Provider):
    def user_is_logged_in(self, request):
        return request.user.is_authenticated()
    
    def user_owns_openid(self, request, openid):
        my_openid_path = reverse('openid_page', args=[request.user.username])
        req = Request(request.environ)
        my_openid = req.application_url + my_openid_path
        return my_openid == openid
    
    def user_trusts_root(self, request, openid, trust_root):
        return True

    def get_sreg_data(self, request, openid):
        return {'email': request.user.email,
                'fullname': request.user.username,
                }

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
def openid_page(request, slug):
    get_object_or_404(User, username=slug)
    return render('openid_page.html', {
        'slug': slug,
        'full_url': request.build_absolute_uri(),
        'server_url': request.build_absolute_uri('/server/'),
    })
