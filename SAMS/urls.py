from django.conf.urls import patterns, include, url
from SAMS.views import login, result, admin, check, student, submit
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^login/$', login),
    (r'^result/$', result),
    (r'^admin/$', admin),
    (r'^check/$', check),
    (r'^class/$', student),
    (r'^submit/$', submit),
    # Examples:
    # url(r'^$', 'SAMS.views.home', name='home'),
    # url(r'^SAMS/', include('SAMS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
