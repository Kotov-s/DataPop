# Generated by Django 4.2 on 2023-05-10 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_alter_message_explanation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explanation',
            name='explanation',
            field=models.TextField(default=''),
        ),
    ]
