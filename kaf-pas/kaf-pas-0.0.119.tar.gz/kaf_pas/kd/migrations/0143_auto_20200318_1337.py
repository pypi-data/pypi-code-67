# Generated by Django 3.0.4 on 2020-03-18 13:37

import bitfield.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kd', '0142_pathes_props'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathes',
            name='props',
            field=bitfield.models.BitField((('enable_upload', 'Директория для закачки'),), db_index=True, default=1),
        ),
    ]
