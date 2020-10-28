# Generated by Django 3.0.7 on 2020-07-04 18:39

import bitfield.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0010_tmp_buffer_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmp_buffer',
            name='props',
            field=bitfield.models.BitField((('posting_nakl', 'Оприходования из накладной'), ('posting_uqv', 'Оприходования из минусов'), ('write_off', 'Списания')), db_index=True, default=0),
        ),
    ]
