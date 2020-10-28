# Generated by Django 3.0.7 on 2020-06-18 19:58

import bitfield.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0242_auto_20200617_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launch_item_refs',
            name='props',
            field=bitfield.models.BitField((('used', 'Доступность в данной производственной спецификации'),), db_index=True, default=1),
        ),
    ]
