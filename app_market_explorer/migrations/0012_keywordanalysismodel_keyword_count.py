# Generated by Django 4.2.7 on 2023-11-19 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_market_explorer', '0011_alter_keyword_ka_model_last_update_serp'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywordanalysismodel',
            name='keyword_count',
            field=models.IntegerField(default=0),
        ),
    ]