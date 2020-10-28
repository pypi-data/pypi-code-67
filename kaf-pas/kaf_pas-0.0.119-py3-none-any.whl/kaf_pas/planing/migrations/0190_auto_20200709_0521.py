# Generated by Django 3.0.8 on 2020-07-09 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0189_operation_operation_version'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='operation_operation',
            constraint=models.UniqueConstraint(condition=models.Q(version=None), fields=('operation', 'production_operation', 'props'), name='Operation_operation_unique_constraint_0'),
        ),
        migrations.AddConstraint(
            model_name='operation_operation',
            constraint=models.UniqueConstraint(fields=('operation', 'production_operation', 'props', 'version'), name='Operation_operation_unique_constraint_1'),
        ),
    ]
