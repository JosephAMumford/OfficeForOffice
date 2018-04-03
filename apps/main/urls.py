from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^generate$', views.generate, name="generate"),
    url(r'^add_quote$', views.add_quote, name="add_quote"),
    url(r'^login$', views.login, name="login"),
    url(r'^process_login$', views.process_login, name="process_login"),
]