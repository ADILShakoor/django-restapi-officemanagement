# Generated by Django 5.1.4 on 2024-12-26 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='Company',
            new_name='company',
        ),
    ]
