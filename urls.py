from django.http import HttpResponse
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # we just need a dummy view to do something
    url(r'^cloak/', include('cloak.urls'))
)
