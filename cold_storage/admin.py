from django.contrib import admin
from django.db import models
from .models import User, farmerDetail, invoice

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'password')

@admin.register(farmerDetail)
class farmerAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'first_name',
                    'last_name', 
                    'address', 
                    'village', 
                    'district',
                    'pincode',
                    'state', 
                    'mobile_no', 
                    'email', 
                    'vehicle_no',
                    'farm_size',
                    'crop_details',
                    'crop_weight',
                    'current_date',
                    'current_time'
    )

@admin.register(invoice)
class invoiceAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'customer_name',
                    'mobile_no',
                    'invoice_date',
                    'item',
                    'total_quantity',
                    'quantity',
                    'unit_price',
                    'total_price',
                    'month_range',
    )




# username --> rushi1724
# email --> rushi91060@gmail.com
# password --> patel4845