# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0009_bpmpaymentmonitor_block_number_scanned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='block_number_scanned',
            field=models.PositiveIntegerField(default=530000),
        ),
    ]
