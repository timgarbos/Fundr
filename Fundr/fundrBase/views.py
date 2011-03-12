from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from Fundr.fundrBase.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect



# Create your views here.

def home(request):
    try:
        projects = Project.objects.all()
    except Project.DoesNotExist:
        raise Http404

    for p in projects:
        #p.features = p.get_active_features()
        p.features = p.top_features()

    return render_to_response('home.html', {'projects':projects},context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', {},context_instance=RequestContext(request))

def profile(request):
    try:
        donations = request.user.donation_set.order_by('created').reverse()[:5]
    except Exception:
        return HttpResponseRedirect('/')
    return render_to_response('profile.html', {'donations':donations},context_instance=RequestContext(request))


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')




def discover(request):
    return render_to_response('discover.html', {},context_instance=RequestContext(request))

@login_required
def create(request):
    return render_to_response('create.html', {},context_instance=RequestContext(request))



def project(request,project_id,**kwargs):
    try:
        p = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404

    try:
        p.memberships = p.membership_set.all()
    except Exception as e:
        print e

    p.features = p.get_active_features()

    return render_to_response('project.html', {'project':p}, context_instance=RequestContext(request))

@login_required
def supportFeature(request,feature_id):
    try:
        f = Feature.objects.get(pk=feature_id)
    except Feature.DoesNotExist:
        raise Http404
    
    d = Donation(feature=f, user=request.user)

    if request.method == 'POST':
        form = DonationForm(request.POST,instance=d)
        if form.is_valid():
            form.save()
            return render_to_response('support_feature_done.html', {'feature':f,'donation':d},context_instance=RequestContext(request))
    else:
        form = DonationForm(instance=d)
    return render_to_response('support_feature.html', {'feature':f,'form':form},context_instance=RequestContext(request))

@login_required
def createProject(request):
    tempProject = Project()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=tempProject)
        if form.is_valid():
            newProject = form.save()
            newMembership = Membership(access='Admin', project=newProject, user=request.user)
            newMembership.save()
            return project(request, newProject.id, msg='Thank you for creating ' + newProject.name + '!')
    else:
        form = ProjectForm(instance=tempProject)
    return render_to_response('create_project.html', {'form':form}, context_instance=RequestContext(request))

@login_required
def request_feature(request, project_id):
    print "Win"
    try:
        p = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        print "Fail"
        #raise Http404

    tempFeature = Feature(project=p, user=request.user)

    if request.method == 'POST':
        form = RequestFeatureForm(request.POST, instance=tempFeature)
        if form.is_valid():
            newFeature = form.save()
            newFeatureStatusEntry = FeatureStatusEntry(feature=newFeature, status='C', goal=100)
            newFeatureStatusEntry.save()
            return project(request, p.id, msg='Thank you for suggesting the feature' + newFeature.name + '!')
    else:
        form = RequestFeatureForm(instance=tempFeature)
    return render_to_response('request_feature.html', {'form':form}, context_instance=RequestContext(request))
