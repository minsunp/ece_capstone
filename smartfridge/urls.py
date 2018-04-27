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
    url(r'^del_shoppingList$', views.del_shoppingList, name='del_shoppingList'),
    url(r'^add_myFridge$', views.add_myFridge, name='add_myFridge'),
    url(r'^get_myFridgeList_json$', views.get_myFridgeList_json, name='get_myFridgeList_json'),
    url(r'^add_to_shoppingList_from_shopping$', views.add_to_shoppingList_from_shopping, name='add_to_shoppingList_from_shopping'),
    url(r'^del_my_fridge$', views.del_my_fridge, name='del_my_fridge'),
    url(r'^receive_barcode/(?P<barcode>[0-9\-]+)$', views.receive_barcode, name='receive_barcode'),
    url(r'^receive_sensor_eggs/(?P<count>\d+)$', views.receive_sensor_eggs, name='receive_sensor_eggs'),
    url(r'^receive_sensor_milk1/(?P<amount>\d+)$', views.receive_sensor_milk1, name='receive_sensor_milk1'),
    url(r'^receive_sensor_milk2/(?P<amount>\d+)$', views.receive_sensor_milk2, name='receive_sensor_milk2'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'smartfridge/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
]