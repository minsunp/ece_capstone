# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# Profile model.
class Profile(models.Model):
    # Take from user input
    bio = models.CharField(max_length=500)
    profile_pic = models.FileField(upload_to="images", blank=True)

    # From system automatically
    content_type = models.CharField(max_length=50, blank=True)
    user_model = models.OneToOneField(User, related_name="user_model")

