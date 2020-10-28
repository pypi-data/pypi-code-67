# Generated by Django 3.0.2 on 2020-01-21 07:44

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0125_auto_20200121_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='precent_item',
            field=isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, to='sales.Precent_items'),
        ),
    ]
