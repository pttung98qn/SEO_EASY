# Generated by Django 4.2.7 on 2023-11-16 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_market_explorer', '0003_rename_serpconfig_serpconfigmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keywordrootmodel',
            name='creator',
        ),
        migrations.AlterField(
            model_name='keywordrootmodel',
            name='keyword',
            field=models.CharField(db_index=True, max_length=125, unique=True),
        ),
    ]
