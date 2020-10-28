# Generated by Django 3.0.3 on 2020-02-08 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0201_auto_20200208_1133'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item_image_refs',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='item_image_refs',
            constraint=models.UniqueConstraint(condition=models.Q(('thumb10', None), ('thumb', None)), fields=('item',), name='Item_image_refs_unique_constraint_0'),
        ),
        migrations.AddConstraint(
            model_name='item_image_refs',
            constraint=models.UniqueConstraint(condition=models.Q(thumb10=None), fields=('item', 'thumb'), name='Item_image_refs_unique_constraint_1'),
        ),
        migrations.AddConstraint(
            model_name='item_image_refs',
            constraint=models.UniqueConstraint(condition=models.Q(thumb=None), fields=('item', 'thumb10'), name='Item_image_refs_unique_constraint_2'),
        ),
        migrations.AddConstraint(
            model_name='item_image_refs',
            constraint=models.UniqueConstraint(fields=('item', 'thumb', 'thumb10'), name='Item_image_refs_unique_constraint_3'),
        ),
    ]
