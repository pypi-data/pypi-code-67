# Generated by Django 3.0.3 on 2020-02-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0216_auto_20200227_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='operations_template_detail',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
