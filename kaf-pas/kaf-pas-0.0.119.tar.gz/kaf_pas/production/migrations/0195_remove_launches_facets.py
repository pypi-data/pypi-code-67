# Generated by Django 3.0.3 on 2020-02-18 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0194_launches_facets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='launches',
            name='facets',
        ),
    ]
