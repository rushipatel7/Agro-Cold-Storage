from django.db import models
from django.db.models import base

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)


class farmerDetail(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=200, blank=True)
    village = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    mobile_no = models.CharField(max_length=15 ,blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    vehicle_no = models.CharField(max_length=50, blank=True, null=True)
    farm_size = models.IntegerField(blank=True, null=True)
    crop_details = models.CharField(max_length=100, blank=True)
    crop_weight = models.IntegerField(blank=True)
    current_date = models.DateField(null=True,blank=True)
    current_time = models.TimeField(null=True, blank=True)

class invoice(models.Model):
    customer_name = models.CharField(max_length=50, blank=True)
    mobile_no = models.CharField(max_length=15, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    item = models.CharField(max_length=50, blank=True)
    total_quantity = models.CharField(max_length=50, blank=True, null=True)  # Farmer Total Weights
    quantity = models.CharField(max_length=50, blank=True)
    unit_price = models.CharField(max_length=50, blank=True, null=True)
    total_price = models.CharField(max_length=50, blank=True, null=True)
    gst_num = models.CharField(max_length=30, null=True, blank=True)
    month_range = models.CharField(max_length=100, null=True, blank=True)

