# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-14 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Nome bolletta')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Prezzo')),
                ('expiry_date', models.DateField(verbose_name='Data di scadenza')),
                ('payed', models.BooleanField(default=False, verbose_name='Pagata')),
                ('payed_date', models.DateField(blank=True, null=True, verbose_name='Data di pagamento')),
                ('payed_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Immagine bollettapagata')),
            ],
            options={
                'verbose_name_plural': 'Bollette',
                'ordering': ('expiry_date',),
                'verbose_name': 'Bolletta',
            },
        ),
    ]
