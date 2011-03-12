from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from Fundr.fundrBase.models import Project
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    try:
        projects = Project.objects.all()
    except Project.DoesNotExist:
        raise Http404
    return render_to_response('site_base.html', {'projects':projects},context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', {},context_instance=RequestContext(request))

def profile(request):
    donations = request.user.donation_set.all()
    return render_to_response('profile.html', {'donations':donations},context_instance=RequestContext(request))
   
   
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')


    
    
def discover(request):
    return render_to_response('discover.html', {},context_instance=RequestContext(request))

@login_required
def create(request):
    return render_to_response('create.html', {},context_instance=RequestContext(request))



def project(request,project_id):
    try:
        p = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404
    
    p.features = p.feature_set.all()
    
    return render_to_response('project.html', {'project':p},context_instance=RequestContext(request))

