# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_auto_20150809_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='bpmtransactions',
            name='nValue',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bpmtransactions',
            name='vout',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='amount_reached_at',
            field=models.DateTimeField(null=True),
        ),
    ]
