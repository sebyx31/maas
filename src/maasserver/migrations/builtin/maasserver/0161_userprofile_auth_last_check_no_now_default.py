# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-23 08:48
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('maasserver', '0160_storage_pools_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='auth_last_check',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
