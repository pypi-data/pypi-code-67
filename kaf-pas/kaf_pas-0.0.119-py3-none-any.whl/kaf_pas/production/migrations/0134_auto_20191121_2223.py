# Generated by Django 2.2.7 on 2019-11-21 22:23

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0133_auto_20191121_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launch_operations_material',
            name='edizm',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to='ckk.Ed_izm'),
        ),
    ]
