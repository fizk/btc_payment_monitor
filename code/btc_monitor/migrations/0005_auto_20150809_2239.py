# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20150809_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='addresses_from',
            field=models.ManyToManyField(to='monitor.BPMAddress_from', null=True),
        ),
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='transactions',
            field=models.ManyToManyField(to='monitor.BPMTransactions', null=True),
        ),
    ]
