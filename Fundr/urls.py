from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'fundrBase.views.home', name='home'),
     url(r'about$', 'fundrBase.views.about', name='about'),
     url(r'projects/(?P<project_id>\d+)/$', 'fundrBase.views.project', name='project'),
    # url(r'^Fundr/', include('Fundr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

   #Dev solution for static files
   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),


    # Malthe socialregistration
    url(r'^', include('socialregistration.urls')),
)
