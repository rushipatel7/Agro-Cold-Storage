from logging import error
from typing import Coroutine
from django.contrib import auth
from django.db.models import query, Q
from django.http.response import Http404
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from email.message import EmailMessage
from supply_chain_management import settings
from twilio.rest import Client
from .forms import farmerRegistrationForm
from .models import farmerDetail, invoice
from .filters import farmerFilter

import datetime
import smtplib


# Create your views here.


# Index page 
def index(request):
    return render(request, 'index.html')


# Admin Login Page
def admin_login(request):
    if request.method == 'POST':
        get_email = request.POST.get('input-username')
        get_pass = request.POST.get('input-pass')

        user = authenticate(username=get_email, password=get_pass)
        if user:
            login(request, user)
            # return redirect('/') # Means Redirect on main first page
            return redirect('dashboard') # Here landing_page is a urls.py landing name
        else:
            error_msg = "Oops...You Cannot access this Page...!! 😐"
            return render(request, 'login.html', {'error_msg':error_msg })
    return render(request, 'login.html')


# Create New Admin
@login_required(login_url='admin-login')
def create_new_admin(request):
    if request.method == 'POST':
        get_username     = request.POST.get('create_username')
        get_email        = request.POST.get('create_email')
        get_pass         = request.POST.get('create_pass')
        get_confirm_pass = request.POST.get('create_confirm_pass')

        

        if get_pass == get_confirm_pass:
            try:
                user = User.objects.get(username =  get_username)
                print("usernae", user)
                return render(request, 'profile.html', {'username_error':'The username you entered has already been taken. Please try another username.'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=get_username, password=get_confirm_pass, email=get_email)
                user.is_superuser = True
                user.is_staff = True
                print("USerValue", user)
                user.save()

                login(request, user)
                return redirect('landing_page')
        else:
            print("Try Again... :(")
            return render(request, 'profile.html')
                
        if user is None :
            user_exist = 'Username already been taken.. please pick up another one :)'
            print("Barabr")
            return render(request, 'profile.html', {'user_exist': user_exist})
        elif user:
            print("Username Same")
    return render(request, 'profile.html')


# Change Password
@login_required(login_url='admin-login')
def change_password(request):
    if request.method == 'POST':
        get_old_pass = request.POST.get('input_oldPass')
        get_new_pass = request.POST.get('input_newPass')
        get_confirm_new_pass = request.POST.get('input_confirmNewPass')

        current_user = request.user.username

        if get_new_pass == get_confirm_new_pass:
            if current_user:
                u = User.objects.get(username__exact=current_user) # Exact data from database ... use __exact query
                u.set_password(get_confirm_new_pass)
                u.save()
                return render(request,'profile.html')
            else:
                return redirect('admin-login')
    return render(request, 'profile.html', {'msg':'Password Change'})


# Forget Password
def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('input-username')
        user  = authenticate(username=username)
        check_username = User.objects.filter(username=username)
        if not check_username:
            not_find_username = 'Username does not exist...!'
            # return render(request,'login.html', {'not_find_username':not_find_username})
            return render(request,'login.html/', {'not_find_username':not_find_username})
        else:
            check_username = User.objects.get(username__exact=username)
            print("KO",str(check_username))
            # Store in session
            request.session['username'] = str(check_username)
            # return redirect('#popup1', kwargs={'check_username':check_username})
            return render(request, 'forget_password.html')
    return render(request, 'login.html')


# def forget_pass(request):
#     # if request.method == 'POST':
#     #     new_pass = request.POST.get('input-pass')
#     #     confirm_pass = request.POST.get('input-confirm-pass')

#         # username = request.session['username']
#         # if new_pass == confirm_pass:
#             # if username:
#             #     u = User.objects.get(username__exact=username) # Exact data from database ... use __exact query
#             #     u.set_password(confirm_pass)
#             #     # u.save()
#             #     return redirect('admin-login')
#             # else:
#             #     return redirect('forget_pass')
#     return render(request, 'forget_password.html')

def forget_password(request):
    if request.method == 'POST':
        new_pass = request.POST.get('input-pass')
        confirm_pass = request.POST.get('input-confirm-pass')

        username = request.session['username']
        print("KN",username)
        if username:
            u = User.objects.get(username__exact=str(username)) # Exact data from database ... use __exact query
            u.set_password(confirm_pass)
            u.save()
            return redirect('admin-login')
        else:
            error_msg = 'Username does not exits...!'
            return render(request, 'forget_password.html', {'error_msg':error_msg})
    return render(request, 'forget_password.html')

def decrypt(string):
    global txt
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")     
        return decoded_text
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


# Logout 
@login_required(login_url='admin-login')
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


# Nav bar common function
def navbar_landing(request):
    # Find last 7 days registration user
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    last_month = today -datetime.timedelta(days=30)
    # last_week_reg = farmerDetail.objects.filter(last_login__range=(last_week, today)) # Use last_login__range to filter last login total user 
    last_week_reg = farmerDetail.objects.filter(Q(current_date__range=(last_week,today)))
    lastweek_user = last_week_reg.count()


    # Now comparison for 2 last week and find percentage
    second_last_week = last_week - datetime.timedelta(days=7)
    second_last_week_reg = farmerDetail.objects.filter(Q(current_date__range=(second_last_week,last_week)))
    second_lastweek_user = second_last_week_reg.count()
    
    total_reg = farmerDetail.objects.count()
    if second_lastweek_user > lastweek_user:
        find_percentage_red = float((total_reg * second_lastweek_user)/total_reg)
        return render(request,'landing.html',{'new_user': lastweek_user,'find_per_red': find_percentage_red,'total_user':total_reg})
    else:
        find_percentage_green = float((total_reg * lastweek_user )/total_reg)
        return render(request,'landing.html',{'new_user': lastweek_user,'find_per_green': find_percentage_green, 'total_user':total_reg})


# Landing Page
@login_required(login_url='admin-login')
def landing(request):
# Find last 7 days registration user
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    last_month = today -datetime.timedelta(days=30)
    # last_week_reg = farmerDetail.objects.filter(last_login__range=(last_week, today)) # Use last_login__range to filter last login total user 
    last_week_reg = farmerDetail.objects.filter(Q(current_date__range=(last_week,today)))
    lastweek_user = last_week_reg.count()


    # Now comparison for 2 last week and find percentage
    second_last_week = last_week - datetime.timedelta(days=7)
    second_last_week_reg = farmerDetail.objects.filter(Q(current_date__range=(second_last_week,last_week)))
    second_lastweek_user = second_last_week_reg.count()
    
    total_reg = farmerDetail.objects.count()
    if second_lastweek_user > lastweek_user:
        find_percentage_red = float((total_reg * second_lastweek_user)/total_reg)
        return render(request,'landing.html',{'new_user': lastweek_user,'find_per_red': find_percentage_red,'total_user':total_reg})
    else:
        find_percentage_green = float((total_reg * lastweek_user )/total_reg)
        return render(request,'landing.html',{'new_user': lastweek_user,'find_per_green': find_percentage_green, 'total_user':total_reg})
    return render(request,'landing.html')

# Dashboard Function
@login_required(login_url='admin-login')
def dashboard(request):
    # Find last 7 days registration user
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    last_month = today -datetime.timedelta(days=30)
    # last_week_reg = farmerDetail.objects.filter(last_login__range=(last_week, today)) # Use last_login__range to filter last login total user 
    last_week_reg = farmerDetail.objects.filter(Q(current_date__range=(last_week,today)))
    lastweek_user = last_week_reg.count()


    # Now comparison for 2 last week and find percentage
    second_last_week = last_week - datetime.timedelta(days=7)
    second_last_week_reg = farmerDetail.objects.filter(Q(current_date__range=(second_last_week,last_week)))
    second_lastweek_user = second_last_week_reg.count()
    
    total_reg = farmerDetail.objects.count()

    jan, feb, march, april, may, june, july, aug, sep, octo, nov, dec = ((datetime.date( today.year, i, 1).strftime('%m')) for i in range(1,13))
    print("JAN",jan)
    print("JAN",feb)
    print("JAN",march)

    
    
    # for i in range(0,7):
        # print("Dates", today - datetime.timedelta(days=i))
    # weekDay = today - datetime.timedelta(days=today.weekday()) # Thresold  
    # print("WeekDay", weekDay)
    first_last_day, second_last_day, third_last_day,fourth_last_day, fiveth_last_day, sixth_last_day, seventh_last_day = (today - datetime.timedelta(days=i) for i in range(0,7))

    print("F",first_last_day)
    print("S",second_last_day)
    print("T",third_last_day)
    
    janu = farmerDetail.objects.filter(Q(current_date__contains=(jan))).count()
    feb = farmerDetail.objects.filter(Q(current_date__contains=(feb))).count()
    mar = farmerDetail.objects.filter(Q(current_date__contains=(march))).count()
    apr = farmerDetail.objects.filter(Q(current_date__contains=(april))).count()
    may = farmerDetail.objects.filter(Q(current_date__contains=(may))).count()
    jun = farmerDetail.objects.filter(Q(current_date__contains=(june))).count()
    jul = farmerDetail.objects.filter(Q(current_date__contains=(july))).count()
    aug = farmerDetail.objects.filter(Q(current_date__contains=(aug))).count()
    sep = farmerDetail.objects.filter(Q(current_date__contains=(sep))).count()
    oct = farmerDetail.objects.filter(Q(current_date__contains=(octo))).count()
    nov = farmerDetail.objects.filter(Q(current_date__contains=(nov))).count()
    dec = farmerDetail.objects.filter(Q(current_date__contains=(dec))).count()

    print("JAN", janu)
    print("FEB", feb)
    print("MAR", mar)

    list_month = {
        'jan': janu,
        'feb': feb,
        'march': mar,
        'april': apr,
        'may': may,
        'jun': jun,
        'july': jul,
        'aug': aug,
        'sep': sep,
        'oct': oct,
        'nov': nov,
        'dec': dec,
    }
    # first_last_day = today - datetime.timedelta(days=1)
    # second_last_day = today - datetime.timedelta(days=2)
    # third_last_day = today - datetime.timedelta(days=3)
    # fourth_last_day = today - datetime.timedelta(days=4)
    # fiveth_last_day = today - datetime.timedelta(days=5)
    # sixth_last_day = today - datetime.timedelta(days=6)
    # seventh_last_day = today - datetime.timedelta(days=7)
    from django.db.models import Sum
    available_weight = invoice.objects.last()
    available_weight = available_weight.total_quantity

    all_weight = farmerDetail.objects.aggregate(Sum('crop_weight'))
    all_weight = all_weight['crop_weight__sum']

    total_sell = invoice.objects.aggregate(Sum('quantity'))
    total_sell = total_sell['quantity__sum']
    # print("ALLL", all_weight.total_quantity)
    if second_lastweek_user > lastweek_user:
        date_wise = farmerDetail.objects.filter(Q(current_date__range=(today,today))).count()

        first_d_w = farmerDetail.objects.filter(Q(current_date__range=(first_last_day, today))).count()
        second_d_w = farmerDetail.objects.filter(Q(current_date__range=(second_last_day, today))).count()
        third_d_w = farmerDetail.objects.filter(Q(current_date__range=(third_last_day, today))).count()
        four_d_w = farmerDetail.objects.filter(Q(current_date__range=(fourth_last_day, today))).count()
        five_d_w = farmerDetail.objects.filter(Q(current_date__range=(fiveth_last_day, today))).count()
        six_d_w = farmerDetail.objects.filter(Q(current_date__range=(sixth_last_day, today))).count()
        seven_d_w = farmerDetail.objects.filter(Q(current_date__range=(seventh_last_day, today))).count()  

        find_percentage_red = float((total_reg * second_lastweek_user)/total_reg)
        return render(request,'dashboard.html',{'new_user': lastweek_user,'find_per_red': find_percentage_red,'total_user':total_reg, 'date_wise':date_wise,
        'first_last_day' : first_d_w,
        'second_last_day' : second_d_w,
        'third_last_day' : third_d_w,
        'four_last_day' : four_d_w,
        'five_last_day' : five_d_w,
        'six_last_day' : six_d_w,
        'seven_last_day' : seven_d_w,
        'all_weight': all_weight,
        'total_sell': total_sell,
        'month': list_month,
        'available_weight': available_weight,
        })
    else:
        date_wise = farmerDetail.objects.filter(Q(current_date__range=(today,today))).count()

        first_d_w = farmerDetail.objects.filter(Q(current_date__range=(first_last_day, today))).count()
        second_d_w = farmerDetail.objects.filter(Q(current_date__range=(second_last_day, today))).count()
        third_d_w = farmerDetail.objects.filter(Q(current_date__range=(third_last_day, today))).count()
        four_d_w = farmerDetail.objects.filter(Q(current_date__range=(fourth_last_day, today))).count()
        five_d_w = farmerDetail.objects.filter(Q(current_date__range=(fiveth_last_day, today))).count()
        six_d_w = farmerDetail.objects.filter(Q(current_date__range=(sixth_last_day, today))).count()
        seven_d_w = farmerDetail.objects.filter(Q(current_date__range=(seventh_last_day, today))).count()        
        find_percentage_green = float((total_reg * lastweek_user )/total_reg)
        return render(request,'dashboard.html',{'new_user': lastweek_user,'find_per_green': find_percentage_green, 'total_user':total_reg, 'date_wise': date_wise,
        'first_last_day' : first_d_w,
        'second_last_day' : second_d_w,
        'third_last_day' : third_d_w,
        'four_last_day' : four_d_w,
        'five_last_day' : five_d_w,
        'six_last_day' : six_d_w,
        'seven_last_day' : seven_d_w,
        'all_weight':all_weight,
        'total_sell': total_sell,
        'month': list_month,
        'available_weight':available_weight,
        })


# Profile
@login_required(login_url='admin-login')
def profile(request):
    if request.method == 'GET': 
        farmer_details = farmerDetail.objects.count()
    return render(request,'profile.html', {'farmer_count': farmer_details})

# SignUp For New Admin
def sign_up(request):
    if request.method == 'POST':
        pass
    return render(request, 'addNewAdmin.html')

def farmer_registration(request):

    
    if request.method == 'POST':

        fr = farmerRegistrationForm(request.POST)
        if fr.is_valid():
            farmer_first_name = fr.cleaned_data['first_name']
            farmer_last_name = fr.cleaned_data['last_name']
            farmer_address =fr.cleaned_data['address']
            farmer_village = fr.cleaned_data['village']
            farmer_district = fr.cleaned_data['district']
            farmer_pincode = fr.cleaned_data['pincode']
            farmer_state = fr.cleaned_data['state']
            farmer_mobile_no = fr.cleaned_data['mobile_no']
            farmer_email = fr.cleaned_data['email']
            farmer_vehicle_no = fr.cleaned_data['vehicle_no']
            farmer_farm_size = fr.cleaned_data['farm_size']
            farmer_crop_details = fr.cleaned_data['crop_details']
            farmer_crop_weight = fr.cleaned_data['crop_weight']

            print("MOBILE NO",farmer_mobile_no)

            # Date and Time
            farmer_reg_date = datetime.datetime.now()
            current_date = str(farmer_reg_date.strftime("%m/%d/%Y"))
            farmer_reg_time = str(farmer_reg_date.strftime("%X"))

            farmer_registration = farmerDetail(first_name=farmer_first_name,
                                               last_name=farmer_last_name,
                                               address=farmer_address,
                                               village=farmer_village,
                                               district=farmer_district,
                                               pincode= farmer_pincode,
                                               state=farmer_state,
                                               mobile_no=farmer_mobile_no,
                                               email=farmer_email,
                                               vehicle_no=farmer_vehicle_no,
                                               farm_size=farmer_farm_size,
                                               crop_details=farmer_crop_details,
                                               crop_weight=farmer_crop_weight,
                                               current_date=farmer_reg_date,
                                               current_time=farmer_reg_time,
            )
            farmer_registration.save()

            # Send Sms
            # account_sid = settings.TWILIO_ACCOUNT_SID
            # auth_token = settings.TWILIO_AUTH_TOKEN
            
            # client = Client(account_sid, auth_token)
            # sms = client.messages.create(
            #     from_=
            # )
            message_to_broadcast = ("you have total {0}(Man) {1} \n" "Date {2} \n" "Time {3}".format(crop_weight,crop_detail,date,time))
            account_sid = 'AC803f4d5bcef1ad59a96501703eaf8f3f'
            auth_token = '610297f40abbb78c37b6f000858b5b66'
            client = Client(account_sid, auth_token)
            to_mobile_num = '+91' + farmer_mobile_no
            print("MOBILE NO",farmer_mobile_no)
            sms = client.messages.create(body=message_to_broadcast,
                                to=str(to_mobile_num),
                                from_= '+18102558277',)

            to_mobile_num = '+91' + farmer_mobile_no
            # sms_send(request=request, crop_weight=farmer_crop_weight, crop_detail=farmer_crop_details ,mobile_no=to_mobile_num, date=farmer_reg_date, time=farmer_reg_time)
            
            subject = "Thanks For Registeration"
            body = "You have total " + str(farmer_crop_weight) + "(Man)"
            fr = farmerRegistrationForm()
            return HttpResponseRedirect('/farmer_data')
    else:
        fr = farmerRegistrationForm()
    return render(request, 'farmer_registration.html',{'form': fr})


# Farmer Registration Using HTML Form
def farmer_reg_html(request):
    if request.method == 'POST':

        farmer_first_name = request.POST.get('input-first-name')
        farmer_last_name = request.POST.get('input-last-name')
        farmer_address =request.POST.get('input-address')
        farmer_village = request.POST.get('input-village')
        farmer_district = request.POST.get('input-district')
        farmer_pincode = request.POST.get('input-pincode')
        farmer_state = request.POST.get('input-state')
        farmer_mobile_no = request.POST.get('input-mobile')
        farmer_email = request.POST.get('input-email')
        farmer_vehicle_no = request.POST.get('input-vehicle-number')
        farmer_farm_size = request.POST.get('input-farm-size')
        farmer_crop_details = request.POST.get('input-crop-details')
        farmer_crop_weight = request.POST.get('input-crop-weight')

        # Date and Time
        farmer_reg_date = datetime.datetime.now()
        current_date = str(farmer_reg_date.strftime("%m/%d/%Y"))
        farmer_reg_time = str(farmer_reg_date.strftime("%X"))

        farmer_registration = farmerDetail(first_name=farmer_first_name,
                                               last_name=farmer_last_name,
                                               address=farmer_address,
                                               village=farmer_village,
                                               district=farmer_district,
                                               pincode= farmer_pincode,
                                               state=farmer_state,
                                               mobile_no=farmer_mobile_no,
                                               email=farmer_email,
                                               vehicle_no=farmer_vehicle_no,
                                            #    farm_size=farmer_farm_size,
                                               crop_details=farmer_crop_details,
                                               crop_weight=farmer_crop_weight,
                                               current_date=farmer_reg_date,
                                               current_time=farmer_reg_time,
            )
        

        to_mobile_num = '+91' + farmer_mobile_no
        # message_to_broadcast = ("you have total {0}(Man) {1} \n" "Date {2} \n" "Time {3}".format(farmer_crop_weight,farmer_crop_details,current_date,farmer_reg_time))
        sms_send(request=request ,crop_weight=farmer_crop_weight, crop_detail=farmer_crop_details ,mobile_no=to_mobile_num, date=farmer_reg_date, time=farmer_reg_time)

        
        farmer_registration.save()
    farmer_count = farmerDetail.objects.count()
    return render(request, 'farmer_registration.html',{'farmer_count':farmer_count})

def farmer_data(request):
    show_data = farmerDetail.objects.all()
    count_data = farmerDetail.objects.filter().count()
    count = 0
    # return render(request, 'farmer_data.html', {'show_data': show_data, 'countData': count_data})
    return render(request, 'tables.html', {'show_data': show_data, 'countData': count_data, 'count': count})


# Update/Edit farmer data function
def update_data(request, id):
    if request.method == 'POST':
        fu = farmerDetail.objects.get(pk=id)
        fr = farmerRegistrationForm(request.POST, instance=fu)
        if fr.is_valid():
            fr.save()
            return HttpResponseRedirect('/farmer_data')
    else:
        fu = farmerDetail.objects.get(pk=id) 
        fr = farmerRegistrationForm(instance=fu)
    return render(request, 'farmer_updateData.html', {'form': fr})


# Delete farmer data function
def delete_data(request,id):
    if request.method == 'POST':
        fd = farmerDetail.objects.get(pk=id)
        fd.delete()

        # app_name = 'cold_storage'
        # from django.core import management
        # management.call_command('sqlsequencereset',app_name)
        return HttpResponseRedirect('/farmer_data')


# Search bar function
def search_data(request):
    if request.method == 'POST':

        # fromDate = request.POST.get('fromDate')
        # toDate = request.POST.get('toDate')
        # searchByDate = farmerDetail.objects.raw('select first_name,last_name,address,village,district,pincode,state,mobile_no,email,vehicle_no,farm_size,crop_details,crop_weight,current_date,current_time from `Farmer details` where current_date between  "'+fromDate+'" and "'+toDate+'" ')
        # print(searchByDate)

        getText = request.POST.get('searchData')
        searchQuery = farmerDetail.objects.filter(Q(mobile_no__contains= getText)   # database ma thi koi value ne fetch krvi hoy to aena 
                                                | Q(email__contains= getText)       # pachd field_Name__contains lagadvu pde
                                                | Q(first_name__contains= getText) 
                                                | Q(last_name__contains= getText) 
                                                | Q(village__contains= getText)
                                                | Q(district__contains= getText)
                                                | Q(state__contains= getText)
                                                | Q(vehicle_no__contains= getText)
                                                | Q(farm_size__contains= getText)
                                                | Q(crop_details__contains= getText)
                                                | Q(crop_weight__contains= getText)
                                                | Q(current_date__contains= getText)
                                                | Q(current_time__contains= getText)
        )
        countNum = searchQuery.count()
        if searchQuery:
            return render(request, 'searchData.html', {'data': searchQuery, 'totalNumRecord': countNum})
        else:
            return redirect('error404') # If user search then no record found in database --> show error code 404


# Search by date 
def search_by_date(request):
    if request.method == 'POST':
        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')
        
        print("DT",fromDate)
            
        # searchQuery = farmerDetail.objects.raw('select * from `Farmer details` where current_date between  "'+fromDate+'" and "'+toDate+'" ')
        searchQuery = farmerDetail.objects.filter(current_date__range=(fromDate,toDate)) #Q(current_date__range=(fromDate,toDate)
        if searchQuery:
            countNum = searchQuery.count()
            return render(request, 'searchData.html', {'data': searchQuery, 'totalNumRecord': countNum})
        else:
            return redirect('error404')
    return render(request, 'searchByDate.html')
    

# Advance Search 
def advance_search(request):
    if request.method == 'POST':
        f_name = request.POST.get('input-first-name')
        l_name = request.POST.get('input-last-name')
        village = request.POST.get('input-village')
        mobile_no = request.POST.get('input-mobile-no')

        searchQuery = farmerDetail.objects.filter(Q(first_name__contains=f_name)
                                                ,Q(last_name__contains=l_name)
                                                , Q(village__contains=village)
                                                , Q(mobile_no__contains=mobile_no))
        if searchQuery:
            countNum = searchQuery.count()
            return render(request, 'searchData.html', {'data': searchQuery, 'totalNumRecord': countNum})
        else:
            return redirect('error404')
    return render(request, 'searchByDate.html')



# Invoice Function
def invoiceData(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        mobile_no = request.POST.get('mob')
        invoice_date = request.POST.get('date')
        item = request.POST.get('item')
        quantity_katta = request.POST.get('quan')
        price_katta = request.POST.get('price')
        total_price = request.POST.get('total_price')
        gst_num = request.POST.get('gst')

        #  Excet All Cold Storage Weights
        
        total_weight = invoice.objects.last()
        total_weight = total_weight.total_quantity

        invoiceDetails = invoice(customer_name= customer_name,
                                mobile_no= mobile_no,
                                invoice_date= invoice_date,
                                item= item,
                                # total_quantity= total_weight,
                                quantity= quantity_katta,
                                unit_price= price_katta,
                                total_price= total_price,
                                gst_num = gst_num,
        )

        if invoiceDetails:
            invoiceDetails.total_quantity = int(total_weight) - int(quantity_katta)
            invoiceDetails.save() 
            invoiceID = invoice.objects.last()
            invoiceID =invoiceID.id
            return redirect('pdfData', id=invoiceID)
    return render(request, 'invoice.html')

# def invoice(request):
#     f_data = farmerDetail.objects.all()
#     if request.method == 'POST':
        
#         mob = request.POST.get('mob')
#         print("Mobile",mob)


#         # Find All Crop Weight
#         from django.db.models import Sum
#         all_weight = farmerDetail.objects.aggregate(Sum('crop_weight'))
#         print("SSS",all_weight['crop_weight__sum'])

#         # searchQuery = farmerDetail.objects.filter(Q(mobile_no__contains= getText)   # database ma thi koi value ne fetch krvi hoy to aena 
#         f_m = farmerDetail.objects.filter(Q(mobile_no__contains= mob))
#         return_weight = request.POST.get('re')


#         for i in f_m:
#             user_id = i.id
#             previous_weight = i.crop_weight

#         # previous_weight = str(previous_weight)
#         left_weight = int(previous_weight) - int(return_weight)

#         if left_weight:
#             new_weight = farmerDetail.objects.get(pk = user_id)
        
#             new_weight.crop_weight = left_weight

#             new_weight.save()
#             return redirect('pdfData', id= user_id)
#         # if f_m:
#         #     return render(request, 'invoice.html', {'de':f_m})
#     return render(request, 'invoice.html', {'data':f_data})

# Email Sending Function
def email_send(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "rushi91060@gmail.com"
    msg['from'] = user
    password = "psebnjhdotssavge"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    # server.quit()


# Send SMS Function
def sms_send(request ,crop_weight, crop_detail ,mobile_no, date, time):
    message_to_broadcast = ("you have total {0}(Man) {1} \n" "Date {2} \n" "Time {3}".format(crop_weight,crop_detail,date,time))
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
    #     if recipient:
    #         client.   messages.create(to=recipient,
    #                                from_=settings.TWILIO_NUMBER,
    #                                body=message_to_broadcast)
    client.messages.create(to=str(mobile_no),
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
    # return HttpResponse("messages sent!", 200)



# Print Data as PDF
from xhtml2pdf import pisa
from django.template.loader import get_template
def render_pdf_view(request,id):
    # fd = farmerDetail.objects.get(pk=id)
    # fd1 = farmerDetail.objects.filter(pk=id)
    fd = invoice.objects.get(pk=id)
    fd1 = invoice.objects.filter(pk=id)

    for i in fd1:
        bond_num = i.id
        # f_name = i.first_name
        # l_name = i .last_name
        # village = i.village
        customer_name = i.customer_name
        quantity = i.quantity
        unit_price = i.unit_price
        total_price = i.total_price
        gst = i.gst_num
        # crop_weight = i.crop_weight

    template_path = 'pdfData.html'


    # context = {'printVar': 'this is template view'}

    invoice_num = bond_num
    katta = quantity # 1 man = 20 Killos
    killo_weight = int(quantity) * int(20)

    print("AAHGA", killo_weight)

    today = datetime.date.today()
    # context = {'printVar': fd1, 'today': today,
    #             'f_name': f_name,
    #             'l_name': l_name,
    #             'village': village,
    #             'bond_number' : bond_number,
    #             'killo_weight' : killo_weight,
    #             'katta' : katta,
    # }

    context = {
        'printVar': fd1,
        'today': today,
        'invoice_number': invoice_num,
        'customer_name': customer_name,
        'quantity': quantity,
        'killo_quantity': int(killo_weight),
        'unit_price': unit_price,
        'gst': gst,
        'total_price': total_price,
    }

    response = HttpResponse(content_type='application/pdf')

    # IF download
    # response['Content-Disposition'] = 'attachment; filename="Report.pdf"'

    # If Display
    response['Content-Disposition'] = 'filename="Report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # Create  a pdf 
    pisa_status = pisa.CreatePDF(
        html, dest=response
    )

    # if error than show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response 

def viewInvoice(request):
    show_data = invoice.objects.all()
    count_data = invoice.objects.filter().count()
    count = 0
    # return render(request, 'farmer_data.html', {'show_data': show_data, 'countData': count_data})
    return render(request, 'viewInvoice.html', {'show_data': show_data, 'countData': count_data, 'count': count})


def searchInvoice(request):
    if request.method == 'POST':
        getText = request.POST.get('searchData')
        print("SGSSG",getText)
        searchQuery = invoice.objects.filter(Q(customer_name__contains= getText)   # database ma thi koi value ne fetch krvi hoy to aena 
                                                | Q(mobile_no__contains= getText)       # pachd field_Name__contains lagadvu pde
                                                | Q(invoice_date__contains= getText) 
                                                | Q(item__contains= getText) 
                                                | Q(quantity__contains= getText)
                                                | Q(unit_price__contains= getText)
        )
        
        countNum = searchQuery.count()
        if searchQuery:
            return render(request, 'searchInvoiceData.html', {'data': searchQuery, 'totalNumRecord': countNum})
        else:
            return redirect('error404') # If user search then no record found in database --> show error code 404

# Error 404
def error404(request):
    return render(request, 'error-404.html')


# Error 500
def error500(request):
    return render(request, 'error-500.html')
