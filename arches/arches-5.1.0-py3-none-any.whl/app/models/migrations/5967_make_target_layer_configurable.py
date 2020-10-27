# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-17 19:51

import os
import uuid
from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [("models", "6481_add_resourceinstance_graphid")]

    operations = [
        migrations.RunSQL(
            """
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{defaultcolor}', '"#F0C200"') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{selectioncolor}', '"#427AFF"') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{hovercolor}', '"#ff0000"') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{colorpalette}', '["#A4DB6E", "#F0C200", "#fdb462", "#22ff33", "#D29EFF"]') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{fillopacity}', '0.2') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{overviewzoom}', '11') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{minzoom}', '15') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{pointradius}', '4') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{linewidth}', '2') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{strokecolor}', '"#fff"') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{strokelinewidth}', '4') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{strokepointradius}', '6') where componentname = 'related-resources-map-card'; 
            update card_components set defaultconfig = jsonb_set(defaultconfig, '{strokepointopacity}', '1') where componentname = 'related-resources-map-card';

            update cards set config = jsonb_set(config, '{defaultcolor}', '"#F0C200"') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{selectioncolor}', '"#427AFF"') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{hovercolor}', '"#ff0000"') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{colorpalette}', '["#A4DB6E", "#F0C200", "#fdb462", "#22ff33", "#D29EFF"]') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{fillopacity}', '0.2') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{overviewzoom}', '11') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{minzoom}', '15') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{pointradius}', '4') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{linewidth}', '2') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{strokecolor}', '"#fff"') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{strokelinewidth}', '4') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{strokepointradius}', '6') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd'; 
            update cards set config = jsonb_set(config, '{strokepointopacity}', '1') where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            """,
            """
            update card_components set defaultconfig = defaultconfig - 'defaultcolor' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'selectioncolor' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'hovercolor' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'colorpalette' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'fillopacity' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'overviewzoom' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'minzoom' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'pointradius' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'linewidth' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'strokecolor' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'strokelinewidth' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'strokepointradius' where componentname = 'related-resources-map-card';
            update card_components set defaultconfig = defaultconfig - 'strokepointopacity' where componentname = 'related-resources-map-card';

            update cards set config = config - 'defaultcolor' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'selectioncolor' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'hovercolor' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'colorpalette' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'fillopacity' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'overviewzoom' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'minzoom' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'pointradius' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'linewidth' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'strokecolor' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'strokelinewidth' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'strokepointradius' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            update cards set config = config - 'strokepointopacity' where componentid = '2d2e0ca3-089c-4f4c-96a5-fb7eb53963bd';
            """,
        )
    ]
