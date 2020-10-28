# Generated by Django 3.0.5 on 2020-04-21 10:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('kd', '0146_auto_20200329_0329'),
        ('ckk', '0224_auto_20200417_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_document',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления')),
                ('editing', models.BooleanField(default=True, verbose_name='Возможность редактирования')),
                ('deliting', models.BooleanField(default=True, verbose_name='Возможность удаления')),
                ('lastmodified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление')),
                ('document', isc_common.fields.related.ForeignKeyProtect(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kd.Documents', verbose_name='Документ')),
                ('item', isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to='ckk.Item')),
                ('lotsman_document', isc_common.fields.related.ForeignKeyProtect(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kd.Lotsman_documents_hierarcy', verbose_name='Документ из Лоцмана')),
            ],
            options={
                'verbose_name': 'Кросс-таблица',
            },
        ),
    ]
