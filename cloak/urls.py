from django.conf.urls import url
from .views import cloak, uncloak, login

urlpatterns = [
    url(r'^cloak$', cloak, name="cloak"),
    url(r'^cloak/(?P<pk>.+)$', cloak, name="cloak"),
    url(r'^uncloak$', uncloak, name="uncloak"),
    url(r'^login/(?P<signature>.*)$', login),
]
