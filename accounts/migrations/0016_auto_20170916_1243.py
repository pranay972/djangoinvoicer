# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 12:43
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20170916_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tax',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bills',
            name='invoice_date',
            field=models.DateField(default=datetime.datetime(2017, 9, 16, 12, 43, 51, 905926, tzinfo=utc)),
        ),
    ]
