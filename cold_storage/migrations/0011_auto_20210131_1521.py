# Generated by Django 3.1.5 on 2021-01-31 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cold_storage', '0010_farmerdetail_current_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerdetail',
            name='mobile_no',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
