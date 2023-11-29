# Generated by Django 4.2.7 on 2023-11-21 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_market_explorer', '0014_kdordermodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SerpModel',
            new_name='KeywordSerpModel',
        ),
        migrations.AddField(
            model_name='kdordermodel',
            name='status',
            field=models.CharField(default='created', max_length=15),
        ),
        migrations.AddField(
            model_name='keywordanalysismodel',
            name='status',
            field=models.CharField(default='running', max_length=25),
        ),
        migrations.AddField(
            model_name='volumeordermodel',
            name='status',
            field=models.CharField(default='created', max_length=15),
        ),
        migrations.CreateModel(
            name='SERPOrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_action', models.CharField(max_length=75)),
                ('id_main', models.IntegerField()),
                ('status', models.CharField(default='created', max_length=15)),
                ('list_obj', models.JSONField()),
                ('order_count', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SERP Order',
            },
        ),
    ]
