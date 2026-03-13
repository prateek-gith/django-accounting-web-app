from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Payment_Index'),
    path('add_pay_voucher/', views.add_payment_voucher, name='Add_Payment_Voucher'),
    path('edit_voucher/<int:v_no>/', views.edit_payment_voucher, name='Edit_Payment_Voucher'),
    path('all_payments/<str:type>/', views.all_payments_detail, name='All_Payments_Voucher'),
    path('update_voucher', views.update_payment_voucher, name='Update_Payments_Voucher'),
]