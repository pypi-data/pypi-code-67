# Generated by Django 2.2.7 on 2019-11-19 14:03

from django.db import migrations
import isc_common.fields.description_field


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0118_launch_item_refs_added_launch'),
    ]

    operations = [
        migrations.AddField(
            model_name='launch_item_refs',
            name='description',
            field=isc_common.fields.description_field.DescriptionField(),
        ),
    ]
