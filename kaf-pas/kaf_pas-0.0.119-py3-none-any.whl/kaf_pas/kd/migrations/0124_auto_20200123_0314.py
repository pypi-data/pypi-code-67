# Generated by Django 3.0.2 on 2020-01-23 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0188_auto_20200122_1619'),
        ('kd', '0123_pathes_attr_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='document_attributes',
            unique_together={('attr_type', 'value_str', 'value_int')},
        ),
    ]
