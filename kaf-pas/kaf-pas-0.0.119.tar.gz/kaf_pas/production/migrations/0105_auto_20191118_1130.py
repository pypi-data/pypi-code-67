# Generated by Django 2.2.7 on 2019-11-18 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0158_delete_status'),
        ('production', '0104_auto_20191118_1127'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='launch_operations_item',
            unique_together={('item', 'num', 'launch')},
        ),
    ]
