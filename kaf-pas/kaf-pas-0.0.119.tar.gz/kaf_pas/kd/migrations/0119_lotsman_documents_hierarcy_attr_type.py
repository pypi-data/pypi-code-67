# Generated by Django 2.2.8 on 2019-12-18 10:13

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0181_auto_20191217_1331'),
        ('kd', '0118_auto_20191217_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotsman_documents_hierarcy',
            name='attr_type',
            field=isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, to='ckk.Attr_type', verbose_name='Тип документа'),
        ),
    ]
