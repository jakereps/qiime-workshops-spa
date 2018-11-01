# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-10 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_workshop_draft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='draft',
            field=models.BooleanField(
                help_text=('Draft workshops do not show up on the workshop '
                           'list overview')),
        ),
    ]
