from django.conf.urls import url
from . import views        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^regis$', views.regis),
    url(r'^login$', views.login),
    url(r'^friends$', views.friends),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^users/(?P<user_id>\d+)$', views.showuser),
    ]
