# Generated by Django 5.0.6 on 2024-07-11 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooks', '0004_alter_single_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='single',
            name='desc',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AddField(
            model_name='teamcook',
            name='desc',
            field=models.CharField(default='', max_length=2000),
        ),
    ]
