# Generated by Django 4.2 on 2023-05-10 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_alter_message_explanation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='explanation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.explanation'),
        ),
    ]