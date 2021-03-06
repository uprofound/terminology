# Generated by Django 3.2.12 on 2022-02-21 18:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nsi', '0004_catalogcontent_unique_catalog_version_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogversion',
            name='start_date',
            field=models.DateField(validators=[django.core.validators.RegexValidator(message='Дата должна быть в формате ГГГГ-ММ-ДД, где ГГГГ-год, ММ-месяц, ДД-день.', regex='(?:199[0-9]|20[012][0-9])-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])')], verbose_name='Дата начала действия'),
        ),
    ]
