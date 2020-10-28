# Generated by Django 3.0.2 on 2020-01-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geostore', '0036_auto_20200116_0926'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='feature',
            index=models.Index(fields=['id', 'layer'], name='geostore_fe_id_bb7476_idx'),
        ),
        migrations.AddIndex(
            model_name='feature',
            index=models.Index(fields=['source', 'layer'], name='geostore_fe_source_cdd710_idx'),
        ),
        migrations.AddIndex(
            model_name='feature',
            index=models.Index(fields=['target', 'layer'], name='geostore_fe_target_b00bb7_idx'),
        ),
    ]
