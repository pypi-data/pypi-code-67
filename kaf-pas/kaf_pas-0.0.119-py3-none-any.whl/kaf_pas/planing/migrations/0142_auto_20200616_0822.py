# Generated by Django 3.0.7 on 2020-06-16 08:22

import bitfield.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0141_auto_20200615_0517'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation_resources_view',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления')),
                ('editing', models.BooleanField(default=True, verbose_name='Возможность редактирования')),
                ('deliting', models.BooleanField(default=True, verbose_name='Возможность удаления')),
                ('lastmodified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление')),
                ('props', bitfield.models.BitField((('inner_routing', 'Связь операций внутри товарной позиции'), ('outer_routing', 'Связь операций между товарными позициями'), ('product_order_routing', 'Связи в блоке задания на производство'), ('product_meking', 'Связи в блоке выпуска')), db_index=True, default=0)),
            ],
            options={
                'verbose_name': 'Ресерсы операций',
                'db_table': 'planing_operation_resources_view',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='operation_refs',
            name='props',
            field=bitfield.models.BitField((('inner_routing', 'Связь операций внутри товарной позиции'), ('outer_routing', 'Связь операций между товарными позициями'), ('product_order_routing', 'Связи в блоке задания на производство'), ('product_meking', 'Связи в блоке выпуска')), db_index=True, default=0),
        ),
    ]
