# Generated by Django 3.0.7 on 2020-06-17 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0242_auto_20200617_0805'),
        ('planing', '0155_auto_20200617_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation_resources',
            old_name='resources',
            new_name='resource',
        ),
        migrations.AlterUniqueTogether(
            name='operation_resources',
            unique_together={('operation', 'resource')},
        ),
    ]
