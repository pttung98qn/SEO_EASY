# Generated by Django 4.2.7 on 2023-11-17 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_market_explorer', '0007_keywordkdmodel_keywordvolumemodel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VolumeOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_action', models.CharField(max_length=75)),
                ('id_main', models.IntegerField()),
                ('list_obj', models.JSONField()),
                ('get_from_date', models.CharField(default='2022-06-30', max_length=15)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Volume Order',
            },
        ),
    ]
