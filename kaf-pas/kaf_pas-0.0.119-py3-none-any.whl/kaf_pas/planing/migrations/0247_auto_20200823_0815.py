# Generated by Django 3.1 on 2020-08-23 08:15

import bitfield.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0246_tmp_operation_value_props'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation_refs',
            name='props',
            field=bitfield.models.BitField((('inner_routing', 'Связь операций внутри товарной позиции'), ('outer_routing', 'Связь операций между товарными позициями'), ('product_order_routing', 'Связи в блоке задания на производство'), ('product_making', 'Связи выпуска'), ('product_making_block', 'Блок операций выпуска, удаляется как одно целое')), db_index=True, default=0),
        ),
    ]
