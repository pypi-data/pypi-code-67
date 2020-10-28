# Generated by Django 3.0.7 on 2020-06-20 14:30

import bitfield.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('planing', '0162_auto_20200618_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation_types',
            name='props',
            field=bitfield.models.BitField((('plus', 'Приходная операция'), ('minus', 'Расходная операция'), ('accounting', 'Операция учета (для подсчета остатков в буферах)')), db_index=True, default=0),
        ),
    ]
