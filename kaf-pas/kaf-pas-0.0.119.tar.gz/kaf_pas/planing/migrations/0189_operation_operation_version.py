# Generated by Django 3.0.8 on 2020-07-09 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0188_operation_operation_props'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation_operation',
            name='version',
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
