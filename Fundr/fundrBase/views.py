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


def dashboard(request):
    try:
        donations = request.user.donation_set.order_by('created').reverse()[:5]
    except Exception:
        return HttpResponseRedirect('/')
    return render_to_response('dashboard.html', {'donations':donations},context_instance=RequestContext(request))

@login_required
def dashboard_feature(request,feature_id):
    try:
        f = Feature.objects.get(pk=feature_id)
    except Feature.DoesNotExist:
        raise Http404
    
    try:
        is_admin = request.user.profile.is_admin_of(f.project)
    except:
        is_admin = False
        
    if not is_admin:
        return HttpResponseRedirect('/')
    
    f.donations = f.donation_set.all()
    
    sum = 0
    x = []
    y = []
    max = 0
    
    for d in f.donations:
        x.append(str(d.created.strftime("%s")))
        sum += d.amount
        if sum > max:
            max = sum
        y.append(str(sum))
    
    minlabelx = str(x[0])
    maxlabelx = str(x[-1])
    minlabely = "0"
    maxlabely = str(max)
    
    linkstring = "https://chart.googleapis.com/chart?chxt=x,y&cht=lxy&chm=B,B4AFAF34,0,0,0&chg=-1,-1,1,3&chs=250x150&chxr=0,"+minlabelx+","+maxlabelx+"|1,"+minlabely+","+maxlabely+"&chds="+minlabelx+","+maxlabelx+","+minlabely+","+maxlabely+"&chd=t:"
    
    linkstring = linkstring + ",".join(x) + "|" + ",".join(y)
    
    return render_to_response('dashboard/feature.html', {'feature':f,'linkstring':linkstring}, context_instance=RequestContext(request))

@login_required
def dashboard_project(request,project_id):
    try:
        p = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404
    
    try:
        is_admin = request.user.profile.is_admin_of(p)
    except:
        is_admin = False
        
    if not is_admin:
        return HttpResponseRedirect('/')
    
    p.features = p.get_active_features()
    p.requested_features = p.get_requested_features()
    
    return render_to_response('dashboard/project.html', {'project':p,'is_admin':is_admin}, context_instance=RequestContext(request))

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
    p.requested_features = p.get_requested_features()

    try:
        is_admin = request.user.profile.is_admin_of(p)
    except:
        is_admin = False

    return render_to_response('project.html', {'project':p, 'is_admin':is_admin}, context_instance=RequestContext(request))



def feature(request,feature_id):
    try:
        f = Feature.objects.get(pk=feature_id)
    except Feature.DoesNotExist:
        raise Http404
    
    try:
        is_admin = request.user.profile.is_admin_of(f.project)
    except:
        is_admin = False
    
    return render_to_response('feature.html', {'feature':f, 'is_admin':is_admin}, context_instance=RequestContext(request))


@login_required
def donate(request,feature_id):
    try:
        f = Feature.objects.get(pk=feature_id)
    except Feature.DoesNotExist:
        raise Http404
    
    d = Donation(feature=f, user=request.user)

    if request.method == 'POST':
        form = DonationForm(request.POST,instance=d)
        if form.is_valid():
            form.save()
            return render_to_response('donate_done.html', {'feature':f,'donation':d},context_instance=RequestContext(request))
    else:
        form = DonationForm(instance=d)
    return render_to_response('donate.html', {'feature':f,'form':form},context_instance=RequestContext(request))

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

    try:
        p = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404

    tempFeature = Feature(project=p, user=request.user)
    tempDonation = Donation(feature=tempFeature, user=request.user)

    if request.method == 'POST':
        request_form = RequestFeatureForm(request.POST, instance=tempFeature)
        donate_form = DonationForm(request.POST, instance=tempDonation)
        if request_form.is_valid() and donate_form.is_valid():
            newFeature = request_form.save()
            newFeatureStatusEntry = FeatureStatusEntry(feature=newFeature, status='R', goal=100)
            newFeatureStatusEntry.save()
            newDonation = Donation(user=request.user, feature=newFeature, amount=donate_form.save(commit=False).amount, comment=donate_form.save(commit=False).comment)
            newDonation.save()
            return project(request, p.id, msg='Thank you for suggesting the feature' + newFeature.name + '!')
    else:
        request_form = RequestFeatureForm(instance=tempFeature)
        donate_form = DonationForm(instance=tempFeature)

    return render_to_response('request_feature.html', {'donate_form':donate_form,'request_form':request_form}, context_instance=RequestContext(request))

@login_required
def edit_feature(request, feature_id):

    try:
        f = Feature.objects.get(pk=feature_id)
    except Feature.DoesNotExist:
        raise Http404

    try:
        if not request.user.profile.is_admin_of(f.project):
            raise Http404
    except:
        raise Http404


    f_status = f.activeStatus()

    if request.method == 'POST':
        feature_form = RequestFeatureForm(request.POST, instance=f)
        status_form = FeatureStatusEntryForm(request.POST, instance=f_status)
        if status_form.is_valid() and feature_form.is_valid():
            f = feature_form.save()
            status_form.feature = f
            status_form.save()
            return project(request, f.project.id, msg='PUDDI PUDDI PUDDI PUDDI PUDDI PUDDI PUDDI PUDDI!!!!!')
    else:
        feature_form = RequestFeatureForm(instance=f)
        status_form = FeatureStatusEntryForm(instance=f_status)
    return render_to_response('edit_feature.html', {'feature':f, 'feature_form':feature_form,'status_form':status_form}, context_instance=RequestContext(request))
