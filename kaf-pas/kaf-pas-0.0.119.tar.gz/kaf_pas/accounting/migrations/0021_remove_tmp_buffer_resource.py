# Generated by Django 3.1 on 2020-08-21 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0020_auto_20200709_0741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tmp_buffer',
            name='resource',
        ),
    ]
