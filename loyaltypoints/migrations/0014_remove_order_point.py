# Generated by Django 3.1.7 on 2021-03-14 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltypoints', '0013_auto_20210314_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='point',
        ),
    ]
