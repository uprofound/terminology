# Generated by Django 3.2.12 on 2022-02-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nsi', '0003_catalogcontent_catalog_version_code_idx'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='catalogcontent',
            constraint=models.UniqueConstraint(fields=('catalog_version', 'code'), name='unique_catalog_version_code'),
        ),
    ]