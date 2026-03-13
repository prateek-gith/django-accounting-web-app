from django.contrib import admin

# Register your models here.

from .models import Sales_Voucher, Sales_Party
admin.site.register(Sales_Voucher)
admin.site.register(Sales_Party)