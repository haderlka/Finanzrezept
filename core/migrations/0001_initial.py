# Generated by Django 5.0.2 on 2025-04-14 19:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalculatorUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calculator_name', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('session_id', models.CharField(blank=True, max_length=100, null=True)),
                ('input_data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['calculator_name'], name='core_calcul_calcula_6378ed_idx'), models.Index(fields=['timestamp'], name='core_calcul_timesta_c5a665_idx')],
            },
        ),
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('referrer', models.URLField(blank=True, null=True)),
                ('session_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['url'], name='core_pagevi_url_1e4370_idx'), models.Index(fields=['timestamp'], name='core_pagevi_timesta_757ebb_idx')],
            },
        ),
    ]
