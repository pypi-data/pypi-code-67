# Generated by Django 2.2.6 on 2019-12-13 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "5668_add_resourceinstancelist"),
    ]

    operations = [
        migrations.AddField(model_name="maplayer", name="searchonly", field=models.BooleanField(default=False),),
    ]
