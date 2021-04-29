"""supply_chain_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from collections import namedtuple
from django.contrib import admin
from django.urls import path
from cold_storage import apiView, views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index),
    path('', views.admin_login, name='admin-login'),
    # path('login/', views.admin_login, name='admin-login'),

    path('newAdmin', views.create_new_admin, name='newAdmin'),

    path('landing/', views.landing, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    # path('farmer_register', views.farmer_registration, name='farmer_registration'),
    path('farmer_register', views.farmer_reg_html, name='farmer_registration'),
    path('farmer_data/', views.farmer_data, name='farmer_data'),
    path('delete/<int:id>', views.delete_data, name='delete_data'),
    
    path('<int:id>', views.update_data, name='update_data'),

    # Ajax to update data url 
    path('farmerUpdate', apiView.farmer_update, name='farmer_update'),


    path('search/', views.search_data, name='search_data'),
    path('search_date/', views.search_by_date, name='search_by_date'),
    path('advance/search/',views.advance_search, name='advance_search'),

    
    path('logout/',views.logout, name='logout'),
    path('password/change/', views.change_password, name='change_password'),
    path('username/check/', views.check_username, name='check_username'),
    path('forget/', views.forget_password, name='forget_pass'),

    #Invoice Url
    path('invoice/', views.invoiceData, name='invoice'),
    path('invoice/view', views.viewInvoice, name='viewInvoice'),
    path('invoice/search/Data', views.searchInvoice, name='search_invoice'),

    # Error Handle Page URLS
    path('404/',views.error404, name='error404'),
    path('500/',views.error500, name='error500'),

    # Print Data in PDF 
    path('view/pdf/<int:id>', views.render_pdf_view, name='pdfData')
]