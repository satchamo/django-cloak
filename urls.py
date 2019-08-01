from django.http import HttpResponse
from django.conf.urls import include, url

urlpatterns = [
    # we just need a dummy view to do something
    url(r'^cloak/', include('cloak.urls'))
]
