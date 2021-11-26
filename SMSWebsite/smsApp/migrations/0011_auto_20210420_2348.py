# Generated by Django 3.2 on 2021-04-20 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsApp', '0010_alter_sms_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='phone_number',
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='sms',
            name='phone_number',
            field=models.CharField(max_length=16),
        ),
    ]
