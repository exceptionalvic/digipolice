# Generated by Django 3.2.6 on 2023-07-23 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_rename_message_infomessage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='infomessage',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RenameField(
            model_name='infomessage',
            old_name='timestamp',
            new_name='created_at',
        ),
    ]
