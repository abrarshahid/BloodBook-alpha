# Generated by Django 3.1.7 on 2021-06-24 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blood_main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='status',
        ),
    ]
