# Generated by Django 5.1.4 on 2025-01-01 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_asset', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='Company',
            new_name='company',
        ),
    ]
