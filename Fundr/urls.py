from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'fundrBase.views.home', name='home'),
     url(r'^about$', 'fundrBase.views.about', name='about'),
     url(r'^project/discover$', 'fundrBase.views.discover', name='discover'),
     url(r'^project/create$', 'fundrBase.views.create_project'),
     url(r'^project/(?P<project_id>\d+)/$', 'fundrBase.views.project', name='project'),
     url(r'^feature/(?P<feature_id>\d+)/$', 'fundrBase.views.feature'),
     url(r'^donate/(?P<feature_id>\d+)/$', 'fundrBase.views.donate'),
     url(r'^feature/request(?P<project_id>\d+)/$', 'fundrBase.views.request_feature'),
     url(r'^feature/edit/(?P<feature_id>\d+)/$', 'fundrBase.views.edit_feature'),
     url(r'^dashboard/?$', 'fundrBase.views.dashboard'),
     url(r'^dashboard/feature/(?P<feature_id>\d+)/$', 'fundrBase.views.dashboard_feature'),
     url(r'^dashboard/project/(?P<project_id>\d+)/$', 'fundrBase.views.dashboard_project'),
    # url(r'^Fundr/', include('Fundr.foo.urls')),
     url(r'^paypal/pdt/', include('paypal.standard.pdt.urls')),

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

   (r'^comments/', include('django.contrib.comments.urls')),

    # Malthe socialregistration
    url(r'^', include('socialregistration.urls')),
)
