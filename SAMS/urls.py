from django.conf.urls import patterns, include, url
import settings
from SAMS.views import nework, profile, login, logout, checkassign, result, admin, check, submit, view, viewAssignment, download, course, classes
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^login/$', login),
    (r'^result/$', result),
    (r'^admin/$', admin),
    (r'^view/$', view),
    (r'^check/$', check),
    #(r'^class/$', student),
    (r'^submit/$', submit),
    (r'^detail/(\d+)/$', viewAssignment),
    (r'^checkassign/(\d+)/$', checkassign),
    (r'^download/(\d+)/$', download),
    (r'^course/(\d+)/$', course),
    (r'^class/(\d+)/$', classes),
    (r'^logout/$', logout),
    (r'^profile/$', profile),
    (r'^add/(\d+)/$', nework),
    (r'^rate/(\d+)/$', rate),
    # Examples:
    # url(r'^$', 'SAMS.views.home', name='home'),
    # url(r'^SAMS/', include('SAMS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
