from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.myFridge, name='myFridge'),
    url(r'^register$', views.register, name='register'),
    url(r'^shopping_list$', views.shopping_list, name='shopping_list'),
    url(r'^your_recipes$', views.your_recipes, name='your_recipes'),
    url(r'^my_profile$', views.my_profile, name='my_profile'),
    url(r'^add_to_shoppingList$', views.add_to_shoppingList, name='add_to_shoppingList'),
    url(r'^get_shoppingList_json$', views.get_shoppingList_json, name='get_shoppingList_json'),


    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'smartfridge/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
]