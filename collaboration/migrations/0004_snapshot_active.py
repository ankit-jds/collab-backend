# Generated by Django 5.1.4 on 2024-12-24 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaboration', '0003_snapshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='snapshot',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
