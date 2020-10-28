# Generated by Django 3.0.3 on 2020-02-11 08:50

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0208_auto_20200210_1259'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='item_refs',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, child=django.db.models.expressions.F('parent')), name='Item_refs_not_circulate_refs'),
        ),
    ]
