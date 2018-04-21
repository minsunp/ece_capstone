# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Profile model.
class Profile(models.Model):
    # Take from user input
    bio = models.CharField(max_length=500)
    profile_pic = models.FileField(upload_to="images", blank=True)

    # From system automatically
    content_type = models.CharField(max_length=50, blank=True)
    user_model = models.OneToOneField(User, related_name="user_model")

# Items in the FRIDGE
class Item(models.Model):
    item_name = models.CharField(max_length=200)
    expiry_date = models.DateField()
    item_count = models.IntegerField()
    # item_img = models.FileField(upload_to="images", blank=True)

# Items in the shopping list
class ShoppingItem(models.Model):
    name = models.CharField(max_length=20)
    count = models.IntegerField()

