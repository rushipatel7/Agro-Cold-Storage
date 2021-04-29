from django import forms
from django.db import models
from django.forms import widgets
from .models import farmerDetail, User

class farmerRegistrationForm(forms.ModelForm):
    """Form definition for farmerRegistration."""

    class Meta:
        """Meta definition for farmerRegistrationform."""

        model = farmerDetail
        fields = ('first_name',
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
        )
        widgets  = {
            'first_name': forms.TextInput(attrs={'class':'form-control', }),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'village': forms.TextInput(attrs={'class':'form-control'}),
            'district': forms.TextInput(attrs={'class':'form-control'}),
            'pincode': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'vehicle_no': forms.TextInput(attrs={'class':'form-control'}),
            'farm_size': forms.TextInput(attrs={'class':'form-control'}),
            'crop_details': forms.TextInput(attrs={'class':'form-control'}),
            'crop_weight': forms.TextInput(attrs={'class':'form-control'}),
        }
