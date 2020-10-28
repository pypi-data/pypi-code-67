# Generated by Django 3.0.3 on 2020-02-08 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0085_auto_20200208_0613'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='operation_refs',
            constraint=models.UniqueConstraint(condition=models.Q(parent=None), fields=('child',), name='Operation_refs_unique_constraint_0'),
        ),
        migrations.AddConstraint(
            model_name='operation_refs',
            constraint=models.UniqueConstraint(fields=('child', 'parent'), name='Operation_refs_unique_constraint_1'),
        ),
    ]
