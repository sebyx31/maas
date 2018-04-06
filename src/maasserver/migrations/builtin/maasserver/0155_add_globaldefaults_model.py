# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-06 00:26
from __future__ import unicode_literals

from django.db import (
    migrations,
    models,
)
import django.db.models.deletion
import maasserver.models.cleansave
import maasserver.models.dnsresource
import maasserver.models.node


class Migration(migrations.Migration):

    dependencies = [
        ('maasserver', '0154_link_usergroup_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('updated', models.DateTimeField(editable=False)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maasserver.Domain')),
            ],
            options={
                'abstract': False,
            },
            bases=(maasserver.models.cleansave.CleanSave, models.Model, object),
        ),
        migrations.AlterField(
            model_name='dnsresource',
            name='domain',
            field=models.ForeignKey(default=maasserver.models.dnsresource.get_default_domain, on_delete=django.db.models.deletion.PROTECT, to='maasserver.Domain'),
        ),
        migrations.AlterField(
            model_name='node',
            name='domain',
            field=models.ForeignKey(blank=True, default=maasserver.models.node.get_default_domain, null=True, on_delete=django.db.models.deletion.PROTECT, to='maasserver.Domain'),
        ),
    ]
