from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^show_dpm/', include('show_dpm.urls')),
    url(r'^admin/', include(admin.site.urls)),

)
