# Generated by Django 3.0.7 on 2020-06-23 05:50

import django.db.models.deletion
from django.db import migrations

import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0228_auto_20200623_0550'),
        ('production', '0247_auto_20200621_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='launch_item_line',
            name='edizm',
            field=isc_common.fields.related.ForeignKeyProtect(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Launchm_line_EdIzm', to='ckk.Ed_izm', verbose_name='Единица измерения'),
        ),
    ]
