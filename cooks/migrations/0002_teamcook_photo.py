# Generated by Django 5.0.6 on 2024-07-09 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamcook',
            name='photo',
            field=models.ImageField(default='', upload_to='uploads/cook/images'),
        ),
    ]
