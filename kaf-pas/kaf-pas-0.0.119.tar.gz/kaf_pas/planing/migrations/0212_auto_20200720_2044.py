# Generated by Django 3.0.8 on 2020-07-20 20:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('production', '0288_auto_20200720_2003'),
        ('planing', '0211_auto_20200720_2043'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='operation_operation',
            unique_together={('operation', 'production_operation')},
        ),
    ]
