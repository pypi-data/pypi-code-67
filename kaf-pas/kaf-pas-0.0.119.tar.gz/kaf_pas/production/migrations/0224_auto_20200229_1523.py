# Generated by Django 3.0.3 on 2020-02-29 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0212_auto_20200225_1013'),
        ('production', '0223_operation_attr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation_attr',
            old_name='attr',
            new_name='attr_type',
        ),
        migrations.AlterUniqueTogether(
            name='operation_attr',
            unique_together={('operation', 'attr_type')},
        ),
    ]
