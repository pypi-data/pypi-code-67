# Generated by Django 3.0.7 on 2020-06-17 19:29

import django.db.models.deletion
from django.db import migrations, models

import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0226_auto_20200421_1007'),
        ('planing', '0157_auto_20200617_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation_material',
            name='edizm',
            field=isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='Operation_material_edizm', to='ckk.Ed_izm'),
        ),
        migrations.AddField(
            model_name='operation_material',
            name='material',
            field=isc_common.fields.related.ForeignKeyProtect(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Operation_material_material', to='ckk.Materials'),
        ),
        migrations.AddField(
            model_name='operation_material',
            name='material_askon',
            field=isc_common.fields.related.ForeignKeyProtect(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Operation_material_material_askon', to='ckk.Material_askon'),
        ),
        migrations.AddField(
            model_name='operation_material',
            name='qty',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=10),
        ),
        migrations.AlterUniqueTogether(
            name='operation_material',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='operation_material',
            constraint=models.UniqueConstraint(condition=models.Q(('material', None), ('material_askon', None)), fields=('operation',), name='Operation_material_unique_constraint_10'),
        ),
        migrations.AddConstraint(
            model_name='operation_material',
            constraint=models.UniqueConstraint(condition=models.Q(material_askon=None), fields=('material', 'operation'), name='Operation_material_unique_constraint_11'),
        ),
        migrations.AddConstraint(
            model_name='operation_material',
            constraint=models.UniqueConstraint(condition=models.Q(material=None), fields=('material_askon', 'operation'), name='Operation_material_unique_constraint_21'),
        ),
        migrations.AddConstraint(
            model_name='operation_material',
            constraint=models.UniqueConstraint(fields=('material', 'material_askon', 'operation'), name='Operation_material_unique_constraint_31'),
        ),
        migrations.RemoveField(
            model_name='operation_material',
            name='launch_operations_material',
        ),
    ]
