# Generated by Django 3.1.7 on 2021-03-21 08:09

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltypoints', '0023_auto_20210321_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(choices=[('Bengaluru', 'Bengaluru'), ('Chennai', 'Chennai'), ('Hyderabad', 'Hyderabad')], max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=phone_field.models.PhoneField(blank=True, max_length=31),
        ),
    ]
