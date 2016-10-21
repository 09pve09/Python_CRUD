from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^validate$', views.process),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^itemrender$', views.itemrender),
    url(r'^wish_items/create$', views.additem),
    url(r'^createitem$', views.createitem),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^wish_items/(?P<id>\d+)$', views.view),
    url(r'^add/(?P<id>\d+)$', views.addfrom),

]
