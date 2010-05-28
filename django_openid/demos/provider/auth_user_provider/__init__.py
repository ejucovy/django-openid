from django_openid.provider import Provider
from django.shortcuts import render_to_response as render
from django.http import HttpResponseRedirect

from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login

from webob import Request

def temporary_login(username, password, request):
    user = authenticate(username=username, password=password)
    if user is None:
        return False
    return True

def openid_login(request):
    if request.method != "POST":
        return HttpResponseRedirect('/server/')
    openid = request.POST['username']
    username = extract_username(openid, request)
    print username
    password = request.POST['password']
    if not temporary_login(username, password, request):
        return HttpResponseRedirect('/server/')
    request.session['openid_login'] = openid
    return HttpResponseRedirect('/server/')


def extract_username(openid_url, request):
    req = Request(request.environ)
    assert openid_url.startswith(req.application_url)
    openid_url = openid_url[len(req.application_url):]
    return openid_url.strip('/')

def extract_user(openid_url, request):
    username = extract_username(openid_url, request)
    return User.objects.get(username=username)

class AuthProvider(Provider):

    save_trusted_root = True

    def user_is_logged_in(self, request):
        return 'openid_login' in request.session
    
    def user_owns_openid(self, request, openid):
        print "Logged in: %s" % request.session['openid_login']
        print "Trying to use: %s" % openid
        ownership = request.session['openid_login'] == openid
        del request.session['openid_login']
        return ownership

    def user_trusts_root(self, request, openid, trust_root):
        return True

    def get_sreg_data(self, request, openid):
        user = extract_user(openid, request)
        return {'email': user.email,
                'fullname': user.username,
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
