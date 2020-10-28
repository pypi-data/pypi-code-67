# Generated by Django 3.0.8 on 2020-07-25 11:10

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0241_delete_standard_colors_view'),
        ('production', '0289_auto_20200721_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation_material',
            name='edizm',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to='ckk.Ed_izm'),
        ),
    ]
