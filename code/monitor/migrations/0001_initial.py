# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BPMAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='BPMAddress_from',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='BPMPaymentMonitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('confirmations_required', models.PositiveSmallIntegerField(default=16)),
                ('cancelled', models.BooleanField(default=False)),
                ('block_number_start', models.PositiveIntegerField()),
                ('block_number_scanned', models.PositiveIntegerField(default=0)),
                ('amount_desired', models.BigIntegerField()),
                ('amount_paid', models.BigIntegerField(default=0)),
                ('goal_reached', models.BooleanField(default=False)),
                ('goal_reached_at', models.DateTimeField(null=True)),
                ('address', models.ForeignKey(to='monitor.BPMAddress')),
                ('addresses_from', models.ManyToManyField(to='monitor.BPMAddress_from')),
            ],
        ),
        migrations.CreateModel(
            name='BPMTransactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_hash', models.CharField(max_length=92)),
                ('vout', models.PositiveIntegerField()),
                ('amount', models.BigIntegerField()),
                ('confirmations', models.BigIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='bpmpaymentmonitor',
            name='transactions',
            field=models.ManyToManyField(to='monitor.BPMTransactions'),
        ),
    ]
