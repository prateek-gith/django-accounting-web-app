from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Purchase_Index'),
    path('add_purchase/', views.add_Purchase_voucher, name='Add_Purchase'),
    path('get_party_details/<str:GSTIN>/', views.get_party_details, name='get_party_details'),
    path('all_purchases/<str:type>/', views.all_Purchase_detail, name='All_Purchases'),
    path('edit/<int:v_no>/', views.edit_voucher, name='Edit_Purchase_Voucher'),
    path('update_purchase', views.update_purchase_voucher, name='Update_Purchase_Voucher'),
    path('get_pdf/<int:v_no>', views.pdf_gen, name='Get_V_PDF'),
]