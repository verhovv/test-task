# Generated by Django 5.1.5 on 2025-01-30 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='letter',
            field=models.CharField(max_length=4096),
        ),
    ]
