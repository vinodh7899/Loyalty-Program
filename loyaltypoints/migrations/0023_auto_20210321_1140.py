# Generated by Django 3.1.7 on 2021-03-21 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltypoints', '0022_auto_20210321_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_details',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(choices=[('Bangalore', 'Bangalore'), ('CHennai', 'CHennai'), ('Hyderabad', 'Hyderabad')], max_length=10),
        ),
    ]
