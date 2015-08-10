# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BPMAddress_from',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_receiving', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='bpmpaymentmonitoring',
            name='addresses_from',
            field=models.ManyToManyField(to='monitor.BPMAddress_from'),
        ),
    ]
