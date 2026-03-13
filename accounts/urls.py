from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_parties, name='Account_Index'),
    path('add_account/', views.index, name='Account_Add_Party'),
    path('edit_account/<int:acc_id>/', views.edit_account, name='Edit_Account'),
    path('update_account/', views.update_account, name='Update_Account'),

]