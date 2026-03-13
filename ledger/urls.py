from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Ledger_Index'),
    # path('day_book', views.dashboard, name='Day_Book'),
    
]