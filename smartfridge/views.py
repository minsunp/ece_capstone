# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
import os

# Create your views here.

##################### My Fridge ###########################
@ensure_csrf_cookie
@login_required
def myFridge(request):
    context = {}

    context['dummy_data_1'] = dummy_data_1
    context['dummy_data_2'] = dummy_data_2
    context['dummy_data_3'] = dummy_data_3
    context['dummy_data_4'] = dummy_data_4

    return render(request, 'smartfridge/myFridge.html', context)

@login_required
def add_myFridge(request):
    print("this should run")
    # Request is always POST
    if request.method != 'POST':
        raise Http404

    # If name is blank,
    if not 'name' in request.POST or not request.POST['name']:
        response_text = {}
        response_text['error'] = 'You must add name to your new item'
        return HttpResponse(json.dumps(response_text), content_type='application/json')

    # If expiry_date is blank,
    if not 'expiry_date' in request.POST or not request.POST['expiry_date']:
        response_text = {}
        response_text['error'] = 'You must add expiry date to your new item'
        return HttpResponse(json.dumps(response_text), content_type='application/json')

    # If count is blank,
    if not 'count' in request.POST or not request.POST['count']:
        response_text = {}
        response_text['error'] = 'You must add count to new item'
        return HttpResponse(json.dumps(response_text), content_type='application/json')

    existing_items = Item.objects.filter(item_name=name)
    if (existing_items.count() == 1): # the item already exists,
        for item in existing_items: # replace all parameters in it, then save
            item.item_name = request.POST['name']
            item.expiry_date=request.POST['expiry_date']
            item.item_count=request.POST['count']
            item.item_amount=request.POST['amount']
            item.save()
    else: # item doesn't exists,
        # Create Item model
        item = Item(item_name=request.POST['name'], expiry_date=request.POST['expiry_date'], item_count=request.POST['count'], item_amount=request.POST['amount'])
        item.save()
    # Send the item info to js - to update my fridge page - need to get rid of this later
    response_text = {}
    response_text['name'] = request.POST['name']
    response_text['expiry_date'] = request.POST['expiry_date']
    response_text['count'] = request.POST['count']
    response_text['amount'] = request.POST['amount']
    # print(json.dumps(response_text))
    return HttpResponse(json.dumps(response_text), content_type='application/json')

#@login_required
def receive_barcode(request, barcode):
    context = {}
    print(barcode)  #print(request.GET["barcode"])
    
    mypath = os.path.dirname(os.path.abspath(__file__))
    #with open(mypath + "/templates/smartfridge/sample_recipe.html")

    dataframe = pd.read_csv(mypath + "/../Grocery_UPC_Database.csv", delimiter=',',)
    #name = (dataframe.loc[[0]]).iloc[0]['name']
    try:
        name = str((dataframe.loc[dataframe['upc12'] == int(barcode)]).iloc[0]['name'])
        print(str(name))
        existing_items = Item.objects.filter(item_name=name)
        if (existing_items.count() == 1):
            for item in existing_items:
                item.item_count = item.item_count + 1
                item.save()
        else:
            item = Item(item_name=name, expiry_date=datetime.datetime.now().strftime("%Y-%m-%d"), item_count=1, item_amount=100)
            item.save()

    # Display the received item name on my fridge
    except:
        pass
    
    return render(request, 'smartfridge/myFridge.html', context)

def receive_sensor_eggs(request, count):
    context = {}
    existing_items = Item.objects.filter(item_name="Eggs")
    # If there's already Eggs, just replace the count
    if (existing_items.count() == 1):
        for item in existing_items:
            item.item_count = count
            item.save()
    else:
        item = Item(item_name="Eggs", expiry_date=datetime.datetime.now().strftime("%Y-%m-%d"), item_count=count, item_amount=100)
        item.save()

    return render(request, 'smartfridge/myFridge.html', context)

def receive_sensor_milk1(request, amount):
    context = {}
    existing_items = Item.objects.filter(item_name="Milk1")
    # If there's already Milk1, just replace the amount
    if (existing_items.count() == 1):
        for item in existing_items:
            # Replace the amount here
            item.item_amount = amount;
            item.save()
    else:
        item = Item(item_name="Milk1", expiry_date=datetime.datetime.now().strftime("%Y-%m-%d"), item_count=1, item_amount=amount)
        item.save()

    return render(request, 'smartfridge/myFridge.html', context)

def receive_sensor_milk2(request, amount):
    context = {}
    existing_items = Item.objects.filter(item_name="Milk2")
    # If there's already Milk2, just replace the amount
    if (existing_items.count() == 1):
        for item in existing_items:
            # Replace the amount here
            item.item_amount = amount;
            item.save()
    else:
        item = Item(item_name="Milk2", expiry_date=datetime.datetime.now().strftime("%Y-%m-%d"), item_count=1, item_amount=amount)
        item.save()

    return render(request, 'smartfridge/myFridge.html', context)

@login_required
def del_my_fridge(request):
    # Request is always POST
    if request.method != 'POST':
        raise Http404

    # If item_id is blank,
    if not 'item_id' in request.POST or not request.POST['item_id']:
        response_text = {}
        response_text['error'] = 'You should select an item to delete'
        return HttpResponse(json.dumps(response_text), content_type='application/json')

    response_text = {}
    # Find the Item model, and delete it
    try:
        item_to_delete = Item.objects.get(id=request.POST['item_id'])
        item_to_delete.delete()
    except ObjectDoesNotExist:
        response_text['error'] = "The item did not exist in the My Fridge List."
    
    # Need to get rid of this part later
    response_text['id'] = request.POST['item_id']
    return HttpResponse(json.dumps(response_text), content_type='application/json')

@login_required
def get_item_from_id(request):
    item = Item.objects.get(id=request.POST['id'])
    this_item = {}
    this_item['name'] = item.item_name
    this_item['expiry_date'] = str(item.expiry_date)
    this_item['count'] = str(item.item_count)
    this_item['amount'] = str(item.item_amount)

    response_text = json.dumps(this_item)
    return HttpResponse(response_text, content_type='application/json')

@login_required
def get_myFridgeList_json(request):
    myFridge_list = []
    allItems = Item.objects.all()
    for item in allItems:
        myFridge_item = {}
        myFridge_item['name'] = item.item_name
        myFridge_item['expiry_date'] = str(item.expiry_date)
        myFridge_item['count'] = str(item.item_count)
        if (item.item_amount != -1):
            myFridge_item['amount'] = str(item.item_amount)
            myFridge_item['has_amount'] = True
        else:
            myFridge_item['has_amount'] = False
        myFridge_item['item_id'] = item.id
        myFridge_list.append(myFridge_item)

    response_text = json.dumps(myFridge_list)
    return HttpResponse(response_text, content_type='application/json')

##################### Shopping List ###########################

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
    if not 'item_id' in request.POST or not request.POST['item_id']:
        response_text = {}
        response_text['error'] = 'You must add content to your shopping list'
        return HttpResponse(json.dumps(response_text), content_type='application/json')

    # Create ShoppingItem model
    item_model = Item.objects.get(id=request.POST['item_id'])
    item = ShoppingItem(name=item_model.item_name, count=1)
    item.save()
    # Send the item info to js - to update shopping list page
    response_text = {}
    response_text['name'] = item_model.item_name
    response_text['count'] = 1
    return HttpResponse(json.dumps(response_text), content_type='application/json')

@login_required
def add_to_shoppingList_from_shopping(request):

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
def del_shoppingList(request):

    # Request is always POST
    if request.method != 'POST':
        raise Http404

    # If item_id is blank,
    if not 'item_id' in request.POST or not request.POST['item_id']:
        response_text = {}
        response_text['error'] = 'You should select an item to delete'
        return HttpResponse(json.dumps(response_text), content_type='application/json')

    response_text = {}
    # Find the ShoppingItem model, and delete it
    try:
        item_to_delete = ShoppingItem.objects.get(id=request.POST['item_id'])
        item_to_delete.delete()
    except ObjectDoesNotExist:
        response_text['error'] = "The item did not exist in the Shopping List."
    
    # Need to get rid of this part later
    response_text['id'] = request.POST['item_id']
    return HttpResponse(json.dumps(response_text), content_type='application/json')

# Put every item in shopping list into json format
@login_required
def get_shoppingList_json(request):
    shopping_list = []
    allItems = ShoppingItem.objects.all()
    for item in allItems:
        shopping_item = {}
        shopping_item['name'] = item.name
        shopping_item['item_id'] = item.id
        shopping_list.append(shopping_item)

    response_text = json.dumps(shopping_list)
    return HttpResponse(response_text, content_type='application/json')

##################### Your Recipes ###########################

from bs4 import BeautifulSoup
import requests
import io
@login_required
def your_recipes(request):
    context = {}
    mypath = os.path.dirname(os.path.abspath(__file__))
    with io.open(mypath + "/templates/smartfridge/sample_recipe.html", "r", encoding="utf-8") as fp:
    #response = requests.get("https://www.delish.com/cooking/recipe-ideas/a19856526/strawberry-shortcake-layer-cake-recipe/")

        soup = BeautifulSoup(fp)

        """
        recipe_image = []
        for image in soup.find_all('div', class_='grid-card-image-container'):
            recipe_image.append(image)

        recipe_text = []
        for text in soup.find_all('div', class_='fixed-recipe-card__info'):
            recipe_text.append(text)
        """
        recipe_text = []
        for span in soup.find_all("span", class_='fixed-recipe-card__title-link'):
            recipe_text.append(span.text.encode("utf-8"))
        #recipe_name = soup.find_all(class_='navbar-brand')

        #recipe_url = []
        #for 

        #context['recipe_image'] = recipe_image
        context['recipe_text'] = recipe_text

    return render(request, 'smartfridge/your_recipes.html', context)

##################### My Profile ###########################

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
