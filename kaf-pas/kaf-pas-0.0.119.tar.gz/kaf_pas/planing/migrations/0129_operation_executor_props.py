# Generated by Django 3.0.7 on 2020-06-07 04:12

import bitfield.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0128_operation_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation_executor',
            name='props',
            field=bitfield.models.BitField((('relevant', 'Актуальность'),), db_index=True, default=1),
        ),
    ]
