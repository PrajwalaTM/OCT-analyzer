# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-04-07 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='image', max_length=500)),
                ('image', models.ImageField(null=True, upload_to='images/', verbose_name='')),
            ],
        ),
    ]
