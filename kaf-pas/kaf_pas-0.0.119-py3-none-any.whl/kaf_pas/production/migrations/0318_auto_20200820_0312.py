# Generated by Django 3.1 on 2020-08-20 03:12

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0317_auto_20200820_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launch_operations_item',
            name='operationitem',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to='production.operations_item'),
        ),
    ]
