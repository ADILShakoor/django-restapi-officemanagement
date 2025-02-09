# Generated by Django 5.1.4 on 2025-02-06 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0002_alter_project_assigned_employees'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='task_images/'),
        ),
        migrations.AddField(
            model_name='task',
            name='weight',
            field=models.IntegerField(default=1),
        ),
    ]
