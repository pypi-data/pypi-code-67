# Generated by Django 3.0.7 on 2020-06-16 15:48

import bitfield.models
from django.contrib.postgres.fields import ArrayField
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('production', '0236_launches_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='launches',
            name='load_part',
            field=ArrayField(base_field=models.PositiveIntegerField(), default=[], size=None),
        ),
        migrations.AddField(
            model_name='launches',
            name='props',
            field=bitfield.models.BitField((('addload', 'запуск в несколько приемов'),), db_index=True, default=0),
        ),
    ]
