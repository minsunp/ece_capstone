# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
import datetime
from smartfridge.forms import RegistrationForm, MyProfileForm
from smartfridge.models import Profile, Item, ShoppingItem
from django.db import transaction
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

##################### Pages ###########################
@login_required
def myFridge(request):
    context = {}

    context['dummy_data_1'] = dummy_data_1
    context['dummy_data_2'] = dummy_data_2
    context['dummy_data_3'] = dummy_data_3
    context['dummy_data_4'] = dummy_data_4

    return render(request, 'smartfridge/myFridge.html', context)

@login_required
def shopping_list(request):
    context = {}

    context['dummy_data_1'] = dummy_data_1
    context['dummy_data_2'] = dummy_data_2
    context['dummy_data_3'] = dummy_data_3
    context['dummy_data_4'] = dummy_data_4
    
    return render(request, 'smartfridge/shopping_list.html', context)

@login_required
def add_to_shoppingList(request):

    # Request is always POST
    if request.method != 'POST':
        raise Http404

    # If item_name is blank,
    if not 'item_name' in request.POST or not request.POST['item_name']:
        response_text = {}
        response_text['error'] = 'You must add content to your shopping list'
        return HttpResponse(json.dumps(response_text), content_type='application/json')

    # Create ShoppingItem model
    item = ShoppingItem(name=request.POST['item_name'], count=1)
    item.save()
    # Send the item info to js - to update shopping list page
    response_text = {}
    response_text['name'] = request.POST['item_name']
    response_text['count'] = 1
    return HttpResponse(json.dumps(response_text), content_type='application/json')

@login_required
def your_recipes(request):
    context = {}

    return render(request, 'smartfridge/your_recipes.html', context)

@login_required
def my_profile(request):
    context = {}

    return render(request, 'smartfridge/my_profile.html', context)



#################### Login & Register ####################
def register(request):
    
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'smartfridge/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'smartfridge/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    # Create Profile model
    new_profile = Profile(bio="Edit your bio here", user_model=new_user)
    new_profile.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('myFridge'))

#################### Dummy Data #########################
dummy_data_1 = {
    'item_name' : 'Milk',
    'expiry_date' : datetime.datetime.now().strftime("%y-%m-%d"),
    'item_count' : 2,
}

dummy_data_2 = {
    'item_name' : 'Eggs',
    'expiry_date' : datetime.datetime.now().strftime("%y-%m-%d"),
    'item_count' : 8,
}

dummy_data_3 = {
    'item_name' : 'Yogurt',
    'expiry_date' : datetime.datetime.now().strftime("%y-%m-%d"),
    'item_count' : 1,
}

dummy_data_4 = {
    'item_name' : 'Apples',
    'expiry_date' : datetime.datetime.now().strftime("%y-%m-%d"),
    'item_count' : 4,
}