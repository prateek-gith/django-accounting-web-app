from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Receipt_Index'),
    path('add_rcpt_voucher/', views.add_receipt_voucher, name='Add_Receipts_Voucher'),
    path('edit_voucher/<int:v_no>/', views.edit_receipt_voucher, name='Edit_Receipt_Voucher'),
    path('all_receipts/<str:type>/', views.all_receipts_detail, name='All_Receipt_Voucher'),
    path('update_voucher', views.update_receipt_voucher, name='Update_Receipt_Voucher'),

]