# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-30 16:43


from django.db import migrations, models
from django.contrib.postgres.fields import JSONField


class Migration(migrations.Migration):

    dependencies = [
        ('models', '4228_plugin_sortorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobilesurveymodel',
            name='onlinebasemaps',
            field=JSONField(blank=True, db_column='onlinebasemaps', null=True),
        ),
    ]
