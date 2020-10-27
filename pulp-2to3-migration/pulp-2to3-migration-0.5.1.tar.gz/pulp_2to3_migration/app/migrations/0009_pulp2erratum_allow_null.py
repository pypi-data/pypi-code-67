# Generated by Django 2.2.11 on 2020-04-06 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulp_2to3_migration', '0008_pulp2srpm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pulp2erratum',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='errata_from',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='errata_type',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='issued',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='pushcount',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='release',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='rights',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='severity',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='solution',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='status',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='summary',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='title',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pulp2erratum',
            name='version',
            field=models.TextField(null=True),
        ),
    ]
