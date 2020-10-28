# Generated by Django 2.2.8 on 2019-12-13 16:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('kd', '0097_auto_20191213_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uploades_lotsman_documents',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления')),
                ('editing', models.BooleanField(default=True, verbose_name='Возможность редактирования')),
                ('deliting', models.BooleanField(default=True, verbose_name='Возможность удаления')),
                ('lastmodified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление')),
                ('document', isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, to='kd.Lotsman_documents')),
                ('upload', isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, to='kd.Uploades')),
            ],
            options={
                'unique_together': {('upload', 'document')},
            },
        ),
    ]
