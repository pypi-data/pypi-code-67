# Generated by Django 3.1.2 on 2020-10-22 09:59

from django.db import migrations


def populate_popup_config(apps, schema_editor):
    LayerModel = apps.get_model("terra_layer", "Layer")
    for layer in LayerModel.objects.all():
        layer.popup_config = {
            "enable": layer.popup_enable,
            "minzoom": layer.popup_minzoom,
            "maxzoom": layer.popup_maxzoom,
            "template": layer.popup_template,
            "wizard": {},
            "advanced": True,
        }


class Migration(migrations.Migration):

    dependencies = [
        ("terra_layer", "0051_layer_popup_config"),
    ]

    operations = [
        migrations.RunPython(
            populate_popup_config,
            reverse_code=migrations.RunPython.noop,
        )
    ]
