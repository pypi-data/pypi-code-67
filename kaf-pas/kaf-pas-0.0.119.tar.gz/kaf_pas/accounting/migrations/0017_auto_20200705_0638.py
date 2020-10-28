# Generated by Django 3.0.7 on 2020-07-05 06:38

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0268_auto_20200628_0808'),
        ('accounting', '0016_tmp_buffer_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmp_buffer',
            name='resource',
            field=isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to='production.Resource'),
        ),
    ]
