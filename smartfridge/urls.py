from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.myFridge, name='myFridge'),

    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'smartfridge/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
]