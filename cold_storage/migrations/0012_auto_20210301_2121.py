# Generated by Django 2.1.15 on 2021-03-01 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cold_storage', '0011_auto_20210131_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerdetail',
            name='farm_size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
