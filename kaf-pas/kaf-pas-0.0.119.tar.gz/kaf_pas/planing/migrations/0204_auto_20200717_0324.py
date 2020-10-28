# Generated by Django 3.0.8 on 2020-07-17 03:24

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planing', '0203_auto_20200717_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation_history',
            name='hcreator',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='operation_operation_history',
            name='hcreator',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
