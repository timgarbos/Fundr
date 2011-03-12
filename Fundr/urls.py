from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'fundrBase.views.home', name='home'),
     url(r'about$', 'fundrBase.views.about', name='about'),
     url(r'projects/discover$', 'fundrBase.views.discover', name='discover'),
     url(r'projects/create$', 'fundrBase.views.create', name='create'),
     url(r'projects/(?P<project_id>\d+)/$', 'fundrBase.views.project', name='project'),
     url(r'feature/(?P<feature_id>\d+)/$', 'fundrBase.views.supportFeature', name='support feature'),
    # url(r'^Fundr/', include('Fundr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'fundrBase.views.logoutUser'),
    (r'^accounts/profile/$', 'fundrBase.views.profile'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

   #Dev solution for static files
   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),


    # Malthe socialregistration
    url(r'^', include('socialregistration.urls')),
)
