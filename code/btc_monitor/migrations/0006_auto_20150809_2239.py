# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20150809_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='addresses_from',
            field=models.ManyToManyField(to='monitor.BPMAddress_from'),
        ),
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='transactions',
            field=models.ManyToManyField(to='monitor.BPMTransactions'),
        ),
    ]
