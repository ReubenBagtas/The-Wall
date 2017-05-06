from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^addtrip', views.addtrip),
    url(r'^tripprocess$', views.tripprocess),
    url(r'^join/(?P<plan_id>\d+)$', views.join),
    url(r'^destination/(?P<plan_id>\d+)$', views.destination)
]