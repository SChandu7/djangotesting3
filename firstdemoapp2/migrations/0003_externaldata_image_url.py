# Generated by Django 5.1.6 on 2025-04-25 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstdemoapp2', '0002_externaldata'),
    ]

    operations = [
        migrations.AddField(
            model_name='externaldata',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
