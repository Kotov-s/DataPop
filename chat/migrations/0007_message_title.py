# Generated by Django 4.2 on 2023-05-04 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_remove_message_changed_csv_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]