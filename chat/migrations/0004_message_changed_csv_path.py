# Generated by Django 4.2 on 2023-05-04 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_threads_csv_path_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='changed_csv_path',
            field=models.CharField(default='', max_length=200),
        ),
    ]