from django.shortcuts import render
from functools import reduce

from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.utils import timezone
import calendar



# Create your views here.

# Import Models
from purchase.models import Purchase_Voucher
from sales.models import Sales_Party, Sales_Voucher
from payments.models import Payment_Voucher
from receipts.models import Receipt_Voucher


def sum_data(accumulator, current_Value):
    return accumulator + current_Value.Sale_To_Amount

    
def sum_data_purchase(accumulator, current_Value):
    return accumulator + current_Value.Purchase_To_Amount

def sum_data_receipt(accumulator, current_Value):
    return accumulator + current_Value.Rcpt_Amount
def sum_data_payment(accumulator, current_Value):
    return accumulator + current_Value.Pay_Amount


def index(request):
    all_Sales_Data = Sales_Voucher.objects.all()
    all_Purchase_Data = Purchase_Voucher.objects.all()
    all_Payment_Data = Payment_Voucher.objects.all()
    all_Receipt_Data = Receipt_Voucher.objects.all()

    total_sale_value = reduce(sum_data, all_Sales_Data,0)
    total_purchase_value = reduce(sum_data_purchase, all_Purchase_Data,0)
    total_receipt_value = reduce(sum_data_receipt, all_Receipt_Data,0)
    total_payment_value = reduce(sum_data_payment, all_Payment_Data,0)


    # for the web line chart which is show on web

    current_year = timezone.now().year

    # SALE monthly data
    sale_data = Sales_Voucher.objects.filter(Sale_Date__year=current_year) \
        .annotate(month=TruncMonth('Sale_Date')).values('month') \
        .annotate(total=Sum('Sale_To_Amount')).order_by('month')

    # PURCHASE monthly data
    purchase_data = Purchase_Voucher.objects.filter(Purchase_Date__year=current_year) \
        .annotate(month=TruncMonth('Purchase_Date')).values('month') \
        .annotate(total=Sum('Purchase_To_Amount')).order_by('month')

    # RECEIPT monthly data
    receipt_data = Receipt_Voucher.objects.filter(Rcpt_Date__year=current_year) \
        .annotate(month=TruncMonth('Rcpt_Date')).values('month') \
        .annotate(total=Sum('Rcpt_Amount')).order_by('month')

    # PAYMENT monthly data
    payment_data = Payment_Voucher.objects.filter(Pay_Date__year=current_year) \
        .annotate(month=TruncMonth('Pay_Date')).values('month') \
        .annotate(total=Sum('Pay_Amount')).order_by('month')

    # Fill missing months with 0
    def format_data(data):
        result = {calendar.month_abbr[i]: 0 for i in range(1, 13)}
        for d in data:
            month_name = d['month'].strftime('%b')
            result[month_name] = d['total']
        return result

    params = {
        'Sales_Data' : all_Sales_Data,
        'Sale_Data': all_Sales_Data, 
        'Total_Sale' : total_sale_value,
        'Total_Purchase' : total_purchase_value, 
        'Total_Receipt' : total_receipt_value, 
        'Total_Payment' : total_payment_value, 
        'Title' : 'Dashboard',
        "months": list(format_data(sale_data).keys()),
        "sale":   list(format_data(sale_data).values()),
        "purchase": list(format_data(purchase_data).values()),
        "receipt": list(format_data(receipt_data).values()),
        "payment": list(format_data(payment_data).values()),

        }

    return render(request, 'dashboard/dashboard.html', params)

