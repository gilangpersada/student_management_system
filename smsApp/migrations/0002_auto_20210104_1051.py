# Generated by Django 3.1.2 on 2021-01-04 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
