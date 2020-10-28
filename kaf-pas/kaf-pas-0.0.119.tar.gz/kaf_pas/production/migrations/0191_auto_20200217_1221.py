# Generated by Django 3.0.3 on 2020-02-17 12:21


from django.db import migrations, models
import django.db.models.deletion
import isc_common.fields.related
from isc_common.fields.code_field import JSONFieldIVC

class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0210_auto_20200212_0752'),
        ('production', '0190_auto_20200217_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='launch_item_refs',
            name='item_full_name',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='launch_item_refs',
            name='item_full_name_obj',
            field=JSONFieldIVC(),
        ),
        migrations.AlterField(
            model_name='launch_item_refs',
            name='item_refs',
            field=isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, to='ckk.Item_refs'),
        ),
    ]
