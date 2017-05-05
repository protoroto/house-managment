# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deadlines', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='person',
            field=models.CharField(blank=True, choices=[('L', 'Leo'), ('I', 'Isa')], max_length=1, null=True, verbose_name='Chi ha speso'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='payed_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data di pagamento'),
        ),
    ]
