# Generated by Django 4.2 on 2023-06-02 15:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_alter_message_explanation'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
