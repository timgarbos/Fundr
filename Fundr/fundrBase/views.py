from django.http import HttpResponse
# Create your views here.

def home(request):
    str = """
{% load facebook_tags %}
{% facebook_button %}
{% facebook_js %}"""
    return HttpResponse(str)
