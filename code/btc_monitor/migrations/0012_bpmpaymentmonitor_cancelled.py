# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0011_auto_20150810_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='bpmpaymentmonitor',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
