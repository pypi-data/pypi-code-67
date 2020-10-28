# Generated by Django 3.0.2 on 2020-01-20 10:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0069_auto_20200119_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operations_view',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления')),
                ('editing', models.BooleanField(default=True, verbose_name='Возможность редактирования')),
                ('deliting', models.BooleanField(default=True, verbose_name='Возможность удаления')),
                ('lastmodified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление')),
                ('value', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('parent_id', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Опреации системные',
                'db_table': 'planing_operations_view',
                'managed': False,
            },
        ),
    ]
