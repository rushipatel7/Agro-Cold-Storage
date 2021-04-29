from django.http.response import JsonResponse
from .models import farmerDetail
from django.views.decorators.csrf import csrf_exempt

# famer update data using ajax and js
@csrf_exempt
def farmer_update(request):
    id = request.POST.get('id','')
    type = request.POST.get('type','')
    value = request.POST.get('value','')

    farmer = farmerDetail.objects.get(id=id)
    if type == "first_name":
        farmer.first_name = value

    if type == "last_name":
        farmer.last_name = value
    
    if type == "address":
        farmer.address = value
    
    if type == "village":
        farmer.village = value
    
    if type == "district":
        farmer.district = value
    
    if type == "pincode":
        farmer.pincode = value
    
    if type == "state":
        farmer.state = value
    
    if type == "mobile_no":
        farmer.mobile_no = value
    
    if type == "email":
        farmer.email = value
    
    if type == "vehicle_no":
        farmer.vehicle_no = value
    
    if type == "farm_size":
        farmer.farm_size = value
    
    if type == "crop_details":
        farmer.crop_details = value
    
    if type == "crop_weight":
        farmer.crop_weight = value

    farmer.save()
    return JsonResponse({"success": "Updated"})