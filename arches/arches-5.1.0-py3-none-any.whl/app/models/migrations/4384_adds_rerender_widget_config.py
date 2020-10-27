# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-07 15:17


from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('models', '4186_graphmodel_slug'),
    ]

    operations = [
        migrations.RunSQL(
            """
            update widgets as w
            set defaultconfig = jsonb_set(defaultconfig, '{rerender}', to_jsonb(true), true)
            where w.name in ('map-widget', 'file-widget', 'iiif-widget');
            """,
            """
            update widgets as w
            set defaultconfig = defaultconfig - 'rerender'
            where w.name in ('map-widget', 'file-widget', 'iiif-widget');
            """)
        ]
