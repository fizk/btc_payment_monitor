# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20150809_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='BPMTransactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_hash', models.CharField(max_length=92)),
            ],
        ),
        migrations.RenameField(
            model_name='bpmaddress',
            old_name='address_receiving',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='bpmaddress_from',
            old_name='address_receiving',
            new_name='address',
        ),
        migrations.AddField(
            model_name='bpmpaymentmonitor',
            name='transactions',
            field=models.ManyToManyField(to='monitor.BPMTransactions'),
        ),
    ]
