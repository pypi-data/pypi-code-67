# Generated by Django 3.0.4 on 2020-03-24 14:34

import bitfield.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0212_auto_20200225_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='props',
            field=bitfield.models.BitField((('relevant', 'Актуальность'), ('from_cdw', 'Получено из чертежа'), ('from_spw', 'Получено из спецификации'), ('for_line', 'Строка спецификации'), ('from_pdf', 'Получено из бумажного архива'), ('man_input', 'Занесено вручную'), ('copied', 'Скопировано'), ('from_lotsman', 'Получено из Лоцмана'), ('enabled', 'Доступность')), db_index=True, default=1),
        ),
    ]
