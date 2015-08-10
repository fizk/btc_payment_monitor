# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0010_auto_20150810_2159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bpmtransactions',
            old_name='nValue',
            new_name='amount',
        ),
        migrations.AddField(
            model_name='bpmtransactions',
            name='confirmations',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='block_number_scanned',
            field=models.PositiveIntegerField(default=500000),
        ),
    ]
