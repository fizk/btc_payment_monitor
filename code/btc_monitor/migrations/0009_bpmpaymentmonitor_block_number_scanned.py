# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_auto_20150810_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='bpmpaymentmonitor',
            name='block_number_scanned',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
