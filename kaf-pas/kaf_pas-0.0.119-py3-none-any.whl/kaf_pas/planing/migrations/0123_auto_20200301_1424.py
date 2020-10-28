# Generated by Django 3.0.3 on 2020-03-01 14:24

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0122_auto_20200301_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='operations',
            name='prev_status',
            field=isc_common.fields.related.ForeignKeyProtect(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='planing_Operations_prev_status', to='planing.Status_operation_types'),
        ),
        migrations.AlterField(
            model_name='operations',
            name='status',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, related_name='planing_Operations_status', to='planing.Status_operation_types'),
        ),
    ]
