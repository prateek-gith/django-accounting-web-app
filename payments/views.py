from django.shortcuts import render, redirect
from sales.models import Sales_Party
from .models import Payment_Voucher

from django.utils import timezone
from functools import reduce

# Create your views here.


def sum_data(num_1,num_2):
    # print("num1: ",num_1, "num2",num_2)
    return num_1 + num_2.Pay_Amount
    
def filter_by_date(my_list):
    return my_list.Pay_Date.month == timezone.now().month

def filter_by_pre_date(my_list):
    return my_list.Pay_Date.month == (timezone.now().month - 1)

def filter_by_today(my_list):
    return my_list.Pay_Date.date() == (timezone.now().date())

def index(request):
    party_data = Sales_Party.objects.all()

    all_payment_voucher = Payment_Voucher.objects.all()


    total_payment_value = reduce(sum_data, all_payment_voucher,0)

    this_months_payment = reduce(sum_data,list(filter(filter_by_date, all_payment_voucher)),0 )


    if (list(filter(filter_by_pre_date, all_payment_voucher))) != []:
        pre_months_payment = reduce(sum_data, (list(filter(filter_by_pre_date, all_payment_voucher))), 0)
    else:
        pre_months_payment = 0

    if (list(filter(filter_by_today, all_payment_voucher))) != []:
        todays_payment = reduce(sum_data, list(filter(filter_by_today, all_payment_voucher)), 0)
    else:
        todays_payment = 0

    parms = {
        'Party_Data' : party_data, 
        'All_Payment_Voucher' : all_payment_voucher, 
        'Total_Payment' : total_payment_value, 
        'This_Month_Payment': this_months_payment, 
        'Pre_Months_RPayment': pre_months_payment, 
        'Todays_Payment':todays_payment, 
        'Title' : 'Payments Dashboard'
    }
    return render(request, 'payments/dashboard.html', parms )

    # return render(request, 'payments/index.html', {'Party_Data' : party_data})


def add_payment_voucher(request):
    party_data = Sales_Party.objects.all()

    if request.method == 'POST':
        party_GSTIN = Sales_Party.objects.filter(Sales_Con_GSTIN = request.POST.get('Party_GSTIN')).first()
        pay_amount = request.POST.get('amount_paid')
        payment_method = request.POST.get('payment_method')
        payment_date = request.POST.get('payment_date')
        payment_description = request.POST.get('description')

        add_voucher = Payment_Voucher(Pay_Party_Data=party_GSTIN, Pay_Date=payment_date, Pay_Method=payment_method,Pay_Amount=pay_amount, Pay_Description=payment_description,)
        add_voucher.save()

    params = {
        'Party_Data' : party_data,
        'Title' : 'Payment Voucher'
    }

    return render(request, 'payments/index.html', params )

def edit_payment_voucher(request,v_no):
    voucher_detail = Payment_Voucher.objects.filter(pk=v_no).first()
    party_data = Sales_Party.objects.all()

    if voucher_detail:
        params = {
            'Voucher_Deatil' : voucher_detail, 
            'Party_Data' :party_data,
            'Title' : 'Edit Payment Voucher'
        }
        return render(request, 'payments/edit_voucher.html', params)
    else:
        return redirect('Add_Payment_Voucher')


def all_payments_detail(request, type):

    if type == 'total_payments':
        all_Payments_Data = Payment_Voucher.objects.all().order_by('-Pay_V_No')
        return render(request, 'payments/all_payments.html', {'All_Payments': all_Payments_Data, 'Type': type.capitalize, 'Title' : f'{type.capitalize().replace('_', " ")} Details'})
    elif type == 'today_payments':
        today = timezone.now().date()
        tomorrow = today + timezone.timedelta(days=1)

        all_Payments_Data = Payment_Voucher.objects.filter( Pay_Date__gte=today, Pay_Date__lt=tomorrow).order_by('-Pay_V_No')
        return render(request, 'payments/all_payments.html', {'All_Payments': all_Payments_Data, 'Type': type.capitalize, 'Title' : f'{type.capitalize().replace('_', " ")} Details'})
    elif type == 'this_payments':
        today = timezone.now()
        all_Payments_Data = Payment_Voucher.objects.filter(Pay_Date__year=today.year,Pay_Date__month=today.month).order_by('-Pay_V_No')
        return render(request, 'payments/all_payments.html', {'All_Payments': all_Payments_Data, 'Type': type.capitalize, 'Title' : f'{type.capitalize().replace('_', " ")} Details'})
    
    elif type == 'pre_payments':
        today = (timezone.now().month -1)
        year = (timezone.now().year)
        all_Payments_Data = Payment_Voucher.objects.filter(Pay_Date__year=year, Pay_Date__month=today).order_by('-Pay_V_No')
        return render(request, 'payments/all_payments.html', {'All_Payments': all_Payments_Data, 'Type': type.capitalize, 'Title' : f'{type.capitalize().replace('_', " ")} Details'})
    else:
        return redirect('Payment_Index')
    

def update_payment_voucher(request):
    if request.method == 'POST':
        party_GSTIN = Sales_Party.objects.filter(Sales_Con_GSTIN = request.POST.get('Party_GSTIN')).first()
        pay_Amount = request.POST.get('amount_paid')
        pay_Method = request.POST.get('payment_method')
        pay_Date = request.POST.get('payment_date')
        pay_Description = request.POST.get('description')
        pay_v_no = Payment_Voucher.objects.filter(Pay_V_No=request.POST.get('payment_v_no')).first()

        pay_v_no.Pay_Party_Data = party_GSTIN
        pay_v_no.Pay_Amount = pay_Amount
        pay_v_no.Pay_Method = pay_Method
        pay_v_no.Pay_Date = pay_Date
        pay_v_no.Pay_Description = pay_Description

        pay_v_no.save()

    return redirect('Payment_Index')

