# Generated by Django 2.0.12 on 2021-03-28 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cold_storage', '0015_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='month_range',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
