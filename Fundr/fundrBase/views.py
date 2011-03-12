from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def home(request):
    return render_to_response('site_base.html', {},context_instance=RequestContext(request))

