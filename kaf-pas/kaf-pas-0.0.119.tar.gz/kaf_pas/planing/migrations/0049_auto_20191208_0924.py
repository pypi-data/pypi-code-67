# Generated by Django 2.2.8 on 2019-12-08 09:24

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0163_locations_users'),
        ('planing', '0048_auto_20191208_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation_locations',
            name='location',
            field=isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='planing_resource_loc', to='ckk.Locations'),
        ),
        migrations.AddField(
            model_name='operation_locations',
            name='operation',
            field=isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='planing_operation_loc', to='planing.Operations'),
        ),
    ]
