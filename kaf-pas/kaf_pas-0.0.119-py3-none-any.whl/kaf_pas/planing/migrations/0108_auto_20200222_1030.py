# Generated by Django 3.0.3 on 2020-02-22 10:30

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0107_auto_20200222_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operations',
            name='status',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to='planing.Status_operation_types'),
        ),
    ]
