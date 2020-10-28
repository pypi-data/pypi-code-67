# Generated by Django 3.1 on 2020-08-04 12:12

import bitfield.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0219_auto_20200801_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation_refs',
            name='props',
            field=bitfield.models.BitField((('inner_routing', 'Связь операций внутри товарной позиции'), ('outer_routing', 'Связь операций между товарными позициями'), ('product_order_routing', 'Связи в блоке задания на производство'), ('product_making', 'Связи выпуска')), db_index=True, default=0),
        ),
    ]
