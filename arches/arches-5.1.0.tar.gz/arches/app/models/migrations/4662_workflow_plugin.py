# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-023-05 14:40


from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('models', '2691_ES_upgrade'),
    ]

    operations = [
        migrations.RunSQL(
            """
        insert into plugins (
                pluginid,
                name,
                icon,
                component,
                componentname,
                config)
            values (
                'e366a702-441e-11e9-9d27-c4b301baab9f',
                'Workflow',
                'fa fa-step-forward',
                'views/components/plugins/workflow',
                'workflow-plugin',
                '{}'
            );
            """,
            """
            delete from plugins where pluginid = 'e366a702-441e-11e9-9d27-c4b301baab9f';
            """)
        ]
