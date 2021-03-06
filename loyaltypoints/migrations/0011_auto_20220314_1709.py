# Generated by Django 3.1.7 on 2022-03-14 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltypoints', '0010_auto_20210312_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='loyaltycoins',
            name='point_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='loyaltypoints.orderitem'),
        ),
    ]
