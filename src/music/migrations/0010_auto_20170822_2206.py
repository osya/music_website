# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-22 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_slug_populate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(default=None, max_length=250, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=models.SlugField(default=None, max_length=250, unique=True),
            preserve_default=False,
        ),
    ]
