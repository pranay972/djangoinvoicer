# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 12:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='invoice_date',
            field=models.DateField(default=datetime.datetime(2017, 9, 20, 12, 14, 32, 752257, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='tax',
            field=models.IntegerField(choices=[(5, 5), (12, 12), (18, 18), (28, 28)]),
        ),
    ]
