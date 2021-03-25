# Generated by Django 3.1.7 on 2021-03-25 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltypoints', '0025_auto_20210321_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='point_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_point', models.IntegerField(default=500)),
                ('to_point', models.IntegerField(default=2000)),
                ('percentage1', models.FloatField(default=0.02)),
                ('percentage2', models.FloatField(default=0.05)),
            ],
        ),
    ]
