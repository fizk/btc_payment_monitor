# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20150809_2239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bpmpaymentmonitor',
            old_name='concluded_at',
            new_name='amount_reached_at',
        ),
        migrations.RemoveField(
            model_name='bpmpaymentmonitor',
            name='concluded',
        ),
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='amount_desired',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='amount_paid',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='block_number_start',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='bpmpaymentmonitor',
            name='confirmations_required',
            field=models.PositiveSmallIntegerField(default=16),
        ),
    ]
