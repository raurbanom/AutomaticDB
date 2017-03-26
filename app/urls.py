from django.conf.urls import url
from app import views
# from app.views import AboutView
# from django.core.urlresolvers import reverse


urlpatterns = [
    # url(r'^$', views.base, name='base'),
    # url(r'^home/$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^manual/$', views.manual, name='manual'),
]