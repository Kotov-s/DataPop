# Generated by Django 4.2 on 2023-06-03 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0019_message_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='threads',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]