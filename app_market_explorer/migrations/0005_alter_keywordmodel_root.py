# Generated by Django 4.2.7 on 2023-11-16 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_market_explorer', '0004_remove_keywordrootmodel_creator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keywordmodel',
            name='root',
            field=models.CharField(max_length=125),
        ),
    ]
