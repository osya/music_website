# pylint: disable=C0103
# Generated by Django 2.0.2 on 2018-02-26 22:13

from django.db import migrations

import autoslug.fields

import album.models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=album.models.get_slug, unique=True),
        ),
    ]
