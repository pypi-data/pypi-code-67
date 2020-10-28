# Generated by Django 3.0.3 on 2020-02-17 14:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0193_auto_20200217_1355'),
        ('planing', '0095_auto_20200217_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation_operation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления')),
                ('editing', models.BooleanField(default=True, verbose_name='Возможность редактирования')),
                ('deliting', models.BooleanField(default=True, verbose_name='Возможность удаления')),
                ('lastmodified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление')),
                ('operation', isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, related_name='planing_operation_2', to='planing.Operations')),
                ('production_operation', isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, related_name='production_operation_2', to='production.Operations')),
            ],
            options={
                'verbose_name': 'Кросс-таблица',
            },
        ),
    ]
