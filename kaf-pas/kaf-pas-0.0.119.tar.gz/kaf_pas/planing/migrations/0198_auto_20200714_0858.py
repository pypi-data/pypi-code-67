# Generated by Django 3.0.8 on 2020-07-14 08:58

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0197_remove_operation_launch_item_level'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Operation_level_view',
        ),
        migrations.DeleteModel(
            name='Operation_location_view',
        ),
        migrations.AddField(
            model_name='operation_launch_item',
            name='operation_refs',
            field=isc_common.fields.related.ForeignKeyCascade(default=None, on_delete=django.db.models.deletion.CASCADE, to='planing.Operation_refs'),
        ),
    ]
