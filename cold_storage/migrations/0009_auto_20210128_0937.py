# Generated by Django 3.1.5 on 2021-01-28 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cold_storage', '0008_remove_farmerdetail_farmername'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmerdetail',
            name='current_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='farmerdetail',
            name='pincode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
