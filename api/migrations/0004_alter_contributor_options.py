# Generated by Django 5.2 on 2025-05-10 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_project_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contributor',
            options={'ordering': ['-created_at']},
        ),
    ]
