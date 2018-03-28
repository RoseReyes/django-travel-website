from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'login$', views.login),
    url(r'^travellanding_page$', views.travellanding_page, name = "home"),
    url(r'^addlanding_page$', views.addlanding_page),
    url(r'^addTravel$', views.addTravel),
    url(r'^createMyTravels$', views.createMyTravels),
    url(r'^destination/(?P<id>\d+)', views.destination),
    url(r'logout$', views.logout, name='my_logout')
]