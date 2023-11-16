# Generated by Django 4.2.7 on 2023-11-16 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api_connector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DFRequestLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_point', models.CharField(max_length=255)),
                ('task_id', models.CharField(max_length=75)),
                ('post_data', models.JSONField()),
                ('res_data', models.JSONField()),
                ('res_status_code', models.IntegerField()),
                ('status_code', models.IntegerField()),
            ],
        ),
    ]
