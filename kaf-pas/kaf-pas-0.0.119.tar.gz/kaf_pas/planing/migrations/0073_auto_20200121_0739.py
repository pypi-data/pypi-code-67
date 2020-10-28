# Generated by Django 3.0.2 on 2020-01-21 07:39

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0072_auto_20200121_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation_refs',
            name='child',
            field=isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, related_name='operation_child', to='planing.Operations'),
        ),
    ]
