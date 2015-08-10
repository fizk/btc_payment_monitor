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
                ('address_receiving', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='BPMPaymentMonitoring',
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
            ],
        ),
    ]
