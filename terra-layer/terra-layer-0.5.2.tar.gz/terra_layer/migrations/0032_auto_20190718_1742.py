# Generated by Django 2.1.9 on 2019-07-18 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("terra_layer", "0031_auto_20190718_1601")]

    operations = [
        migrations.AlterUniqueTogether(
            name="layergroup", unique_together={("view", "label", "parent")}
        )
    ]
