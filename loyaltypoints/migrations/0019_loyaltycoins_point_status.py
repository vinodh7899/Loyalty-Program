# Generated by Django 3.1.7 on 2021-03-19 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltypoints', '0018_loyaltycoins_points_redeem'),
    ]

    operations = [
        migrations.AddField(
            model_name='loyaltycoins',
            name='point_status',
            field=models.BooleanField(default=False),
        ),
    ]
