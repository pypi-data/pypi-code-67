# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-09 22:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from ..models.base import ManyToManyFieldACL


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_usergroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aclpermission',
            name='uagroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.UserGroup'),
        ),
        migrations.AlterField(
            model_name='group',
            name='hosts',
            field=ManyToManyFieldACL(related_name='groups', related_query_name='groups', to='main.Host'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='hosts',
            field=ManyToManyFieldACL(related_name='inventories', to='main.Host'),
        ),
        migrations.AlterField(
            model_name='project',
            name='hosts',
            field=ManyToManyFieldACL(blank=True, null=True, related_name='projects', to='main.Host'),
        ),
    ]
