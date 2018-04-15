# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-14 23:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartfridge', '0002_auto_20180414_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_model',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_model', to=settings.AUTH_USER_MODEL),
        ),
    ]
