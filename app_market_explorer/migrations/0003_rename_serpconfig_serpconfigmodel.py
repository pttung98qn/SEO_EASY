# Generated by Django 4.2.7 on 2023-11-16 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_market_explorer', '0002_domainmodel_alter_keywordanalysismodel_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SerpConfig',
            new_name='SerpConfigModel',
        ),
    ]