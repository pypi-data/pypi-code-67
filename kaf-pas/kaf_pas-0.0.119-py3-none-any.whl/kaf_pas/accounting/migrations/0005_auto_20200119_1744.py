# Generated by Django 3.0.2 on 2020-01-19 17:44

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0185_auto_20200117_1305'),
        ('accounting', '0004_tmp_buffer_edizm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmp_buffer',
            name='edizm',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to='ckk.Ed_izm'),
        ),
    ]
