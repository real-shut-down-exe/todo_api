# Generated by Django 4.2.7 on 2023-11-10 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectionRequest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectionrequest',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]