# Generated by Django 3.0.7 on 2020-06-27 15:05

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0228_auto_20200623_0550'),
        ('production', '0262_auto_20200627_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='launch_operation_attr',
            name='launch_operationitem',
        ),
        migrations.AddField(
            model_name='launch_operation_attr',
            name='launch',
            field=isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, to='production.Launches'),
        ),
        migrations.AddField(
            model_name='launch_operation_attr',
            name='operation',
            field=isc_common.fields.related.ForeignKeyCascade(default=None, on_delete=django.db.models.deletion.CASCADE, to='production.Operations'),
        ),
        migrations.AlterField(
            model_name='launch_operation_attr',
            name='attr_type',
            field=isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, to='ckk.Attr_type'),
        ),
    ]
