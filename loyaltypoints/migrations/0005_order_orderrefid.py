# Generated by Django 3.1.7 on 2021-03-10 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltypoints', '0004_auto_20210310_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderrefid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
