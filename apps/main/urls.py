from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^get_count$', views.get_count, name="get_count"),
    url(r'^get_quotes$', views.get_quotes, name="get_quotes"),
    url(r'^add_quote$', views.add_quote, name="add_quote"),
    url(r'^add$', views.add, name="add"),
    url(r'^login$', views.login, name="login"),
    url(r'^process_login$', views.process_login, name="process_login"),
]