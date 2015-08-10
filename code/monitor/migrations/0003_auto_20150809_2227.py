# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20150809_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='BPMPaymentMonitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('confirmations_required', models.SmallIntegerField(default=16)),
                ('block_number_start', models.IntegerField()),
                ('amount_desired', models.IntegerField()),
                ('amount_paid', models.IntegerField()),
                ('amount_reached', models.BooleanField(default=False)),
                ('concluded', models.BooleanField(default=False)),
                ('concluded_at', models.DateTimeField()),
                ('address', models.ForeignKey(to='monitor.BPMAddress')),
                ('addresses_from', models.ManyToManyField(to='monitor.BPMAddress_from')),
            ],
        ),
        migrations.RemoveField(
            model_name='bpmpaymentmonitoring',
            name='address',
        ),
        migrations.RemoveField(
            model_name='bpmpaymentmonitoring',
            name='addresses_from',
        ),
        migrations.DeleteModel(
            name='BPMPaymentMonitoring',
        ),
    ]
