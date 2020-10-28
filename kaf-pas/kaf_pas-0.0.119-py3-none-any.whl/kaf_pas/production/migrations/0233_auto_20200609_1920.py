# Generated by Django 3.0.7 on 2020-06-09 19:20

from django.db import migrations, models
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0129_demand_qty_for_launch'),
        ('production', '0232_auto_20200606_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launches',
            name='demand',
            field=isc_common.fields.related.ForeignKeyProtect(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sales.Demand'),
        ),
        migrations.AlterField(
            model_name='launches',
            name='qty',
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
