# Generated by Django 2.2.3 on 2019-07-09 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0050_customer_long_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='full_name',
        ),
    ]
