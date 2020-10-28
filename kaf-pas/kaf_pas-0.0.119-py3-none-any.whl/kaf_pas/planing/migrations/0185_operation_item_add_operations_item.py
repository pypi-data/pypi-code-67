# Generated by Django 3.0.8 on 2020-07-08 15:17

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0271_auto_20200706_1130'),
        ('planing', '0184_auto_20200707_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation_item_add',
            name='operations_item',
            field=isc_common.fields.related.ForeignKeyCascade(default=None, on_delete=django.db.models.deletion.CASCADE, to='production.Launch_operations_item'),
        ),
    ]
