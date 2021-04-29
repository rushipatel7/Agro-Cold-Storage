from .models import farmerDetail
import django_filters

class farmerFilter(django_filters.FilterSet):
    class Meta:
        model = farmerDetail
        # fields = ['first_name',
        #             'last_name', 
        #             'address', 
        #             'village', 
        #             'district', 
        #             'state', 
        #             'mobile_no', 
        #             'email', 
        #             'vehicle_no',
        #             'farm_size',
        #             'crop_details',
        #             'crop_weight'
        # ]
        fields = '__all__'