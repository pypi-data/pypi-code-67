# Generated by Django 2.2 on 2019-04-16 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0022_auto_20190416_1014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item_line',
            old_name='item_child',
            new_name='child',
        ),
        migrations.RenameField(
            model_name='item_line',
            old_name='item_parent',
            new_name='parent',
        ),
    ]
