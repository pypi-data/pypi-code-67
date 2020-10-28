# Generated by Django 2.2.16 on 2020-09-09 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mapbox_baselayer", "0005_auto_20191202_1840"),
        ("terra_layer", "0049_auto_20200316_1124"),
    ]

    operations = [
        migrations.AddField(
            model_name="scene",
            name="baselayer",
            field=models.ManyToManyField(to="mapbox_baselayer.MapBaseLayer"),
        ),
    ]
