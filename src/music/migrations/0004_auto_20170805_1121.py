# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20170801_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
