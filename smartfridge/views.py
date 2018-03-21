# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def myFridge(request):
    context = {}

    return render(request, 'smartfridge/myFridge.html', context)

