# Generated by Django 3.0.3 on 2020-02-24 04:13

from django.db import migrations, models
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0110_auto_20200223_1636'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='operation_refs',
            name='Operation_refs_unique_constraint_0',
        ),
        migrations.RemoveConstraint(
            model_name='operation_refs',
            name='Operation_refs_unique_constraint_1',
        ),
        migrations.AddField(
            model_name='operation_refs',
            name='parent_real',
            field=isc_common.fields.related.ForeignKeyProtect(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operation_parent_real', to='planing.Operations'),
        ),
        migrations.AddConstraint(
            model_name='operation_refs',
            constraint=models.UniqueConstraint(condition=models.Q(('parent', None), ('parent_real', None)), fields=('child',), name='Operation_refs_unique_constraint_0'),
        ),
        migrations.AddConstraint(
            model_name='operation_refs',
            constraint=models.UniqueConstraint(condition=models.Q(parent_real=None), fields=('child', 'parent'), name='Operation_refs_unique_constraint_1'),
        ),
        migrations.AddConstraint(
            model_name='operation_refs',
            constraint=models.UniqueConstraint(condition=models.Q(parent=None), fields=('child', 'parent_real'), name='Operation_refs_unique_constraint_2'),
        ),
        migrations.AddConstraint(
            model_name='operation_refs',
            constraint=models.UniqueConstraint(fields=('child', 'parent', 'parent_real'), name='Operation_refs_unique_constraint_3'),
        ),
    ]
