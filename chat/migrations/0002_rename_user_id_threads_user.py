# Generated by Django 4.2 on 2023-05-04 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='threads',
            old_name='user_id',
            new_name='user',
        ),
    ]
