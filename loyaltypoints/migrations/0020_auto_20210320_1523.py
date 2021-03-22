# Generated by Django 3.1.7 on 2021-03-20 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltypoints', '0019_loyaltycoins_point_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(default=-1, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
