from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
    url(r'^$','show_dpm.views.index'),
    url(r'^show_dpm/$','show_dpm.views.index'),
    url(r'^boston/$','show_dpm.views.visualize_boston'),
    url(r'([0-9]+)','show_dpm.views.show_pic'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
