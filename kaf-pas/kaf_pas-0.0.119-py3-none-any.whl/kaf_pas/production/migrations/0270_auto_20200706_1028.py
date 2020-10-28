# Generated by Django 3.0.8 on 2020-07-06 10:28

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0229_locations_view'),
        ('production', '0269_auto_20200706_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='launch_operation_resources',
            name='location_fin',
            field=isc_common.fields.related.ForeignKeyProtect(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Launch_operation_resources_location_fin', to='ckk.Locations'),
        ),
        migrations.AlterField(
            model_name='launch_operation_resources',
            name='location',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, related_name='Launch_operation_resources_location', to='ckk.Locations'),
        ),
    ]
