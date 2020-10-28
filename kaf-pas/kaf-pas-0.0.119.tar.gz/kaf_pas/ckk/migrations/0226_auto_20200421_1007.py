# Generated by Django 3.0.5 on 2020-04-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0225_item_document'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='item_document',
            constraint=models.UniqueConstraint(condition=models.Q(('document', None), ('lotsman_document', None)), fields=('item',), name='Item_document_unique_constraint_0'),
        ),
        migrations.AddConstraint(
            model_name='item_document',
            constraint=models.UniqueConstraint(condition=models.Q(lotsman_document=None), fields=('document', 'item'), name='Item_document_unique_constraint_1'),
        ),
        migrations.AddConstraint(
            model_name='item_document',
            constraint=models.UniqueConstraint(condition=models.Q(document=None), fields=('item', 'lotsman_document'), name='Item_document_unique_constraint_2'),
        ),
        migrations.AddConstraint(
            model_name='item_document',
            constraint=models.UniqueConstraint(fields=('document', 'item', 'lotsman_document'), name='Item_document_unique_constraint_3'),
        ),
    ]
