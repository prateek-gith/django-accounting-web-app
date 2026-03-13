from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Sale_Index'),
    path('add_sale/', views.add_sale_voucher, name='Add_Sale'),
    path('get_party_details/<str:GSTIN>/', views.get_party_details, name='get_party_details'),
    path('all_sales/<str:type>/', views.all_sales_detail, name='All_Sales'),
    path('edit/<int:v_no>/', views.edit_voucher, name='Edit_Sale_Voucher'),
    path('update_sale', views.update_sale_voucher, name='Update_Sale_Voucher'),
    path('get_pdf/<int:v_no>', views.pdf_gen, name='Get_V_PDF'),
]