# Generated by Django 4.2.7 on 2023-11-10 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connectionRequest', '0002_connectionrequest_is_accepted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connectionrequest',
            old_name='date',
            new_name='created_at',
        ),
    ]