# Generated by Django 3.0.8 on 2020-07-20 19:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ckk', '0239_delete_item_refs_history'),
        ('production', '0286_auto_20200720_1527'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='operations_item',
            unique_together={('item', 'operation')},
        ),
    ]
