# Generated by Django 2.2.7 on 2019-11-21 06:23

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0013_auto_20191121_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launch_item_refs_timing',
            name='ed_izm',
            field=isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, to='ckk.Ed_izm'),
        ),
    ]
