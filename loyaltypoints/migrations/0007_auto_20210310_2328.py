# Generated by Django 3.1.7 on 2021-03-10 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltypoints', '0006_auto_20210310_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='point',
        ),
        migrations.AddField(
            model_name='order',
            name='point',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loyaltypoints.loyaltycoins'),
        ),
    ]
