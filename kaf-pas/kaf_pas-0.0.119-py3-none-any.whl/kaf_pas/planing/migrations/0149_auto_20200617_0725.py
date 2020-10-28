# Generated by Django 3.0.7 on 2020-06-17 07:25

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0241_auto_20200617_0705'),
        ('planing', '0148_auto_20200617_0724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation_resources',
            name='resource',
        ),
        migrations.AddField(
            model_name='operation_resources',
            name='launch_operation_resources',
            field=isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='planing_resource_res', to='production.Launch_operation_resources'),
        ),
    ]
