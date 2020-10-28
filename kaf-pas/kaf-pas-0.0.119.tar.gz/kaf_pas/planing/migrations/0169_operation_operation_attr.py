# Generated by Django 3.0.7 on 2020-06-24 15:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0228_auto_20200623_0550'),
        ('planing', '0168_auto_20200623_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation_operation_attr',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления')),
                ('editing', models.BooleanField(default=True, verbose_name='Возможность редактирования')),
                ('deliting', models.BooleanField(default=True, verbose_name='Возможность удаления')),
                ('lastmodified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление')),
                ('attr_type', isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to='ckk.Attr_type')),
                ('operation', isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, to='planing.Operations')),
            ],
            options={
                'verbose_name': 'Кросс таблица',
                'unique_together': {('operation', 'attr_type')},
            },
        ),
    ]
