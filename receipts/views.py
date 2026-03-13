from django.shortcuts import render, redirect
from sales.models import Sales_Party
from .models import Receipt_Voucher

from django.utils import timezone
from functools import reduce



# Create your views here.




def sum_data(num_1,num_2):
    # print("num1: ",num_1, "num2",num_2)
    return num_1 + num_2.Rcpt_Amount
    
def filter_by_date(my_list):
    return my_list.Rcpt_Date.month == timezone.now().month

def filter_by_pre_date(my_list):
    return my_list.Rcpt_Date.month == (timezone.now().month - 1)

def filter_by_today(my_list):
    return my_list.Rcpt_Date.date() == (timezone.now().date())

def index(request):
    party_data = Sales_Party.objects.all()
    all_receipt_voucher = Receipt_Voucher.objects.all()

    total_receipt_value = reduce(sum_data, all_receipt_voucher,0)

    this_months_receipt = reduce(sum_data,list(filter(filter_by_date, all_receipt_voucher)),0 )


    if (list(filter(filter_by_pre_date, all_receipt_voucher))) != []:
        pre_months_receipt = reduce(sum_data, (list(filter(filter_by_pre_date, all_receipt_voucher))), 0)
    else:
        pre_months_receipt = 0

    if (list(filter(filter_by_today, all_receipt_voucher))) != []:
        todays_receipt = reduce(sum_data, list(filter(filter_by_today, all_receipt_voucher)), 0)
    else:
        todays_receipt = 0

    params = {
        'Party_Data' : party_data, 
        'All_Receipt_Voucher' : all_receipt_voucher, 
        'Total_Receipt' : total_receipt_value, 
        'This_Month_Receipt': this_months_receipt, 
        'Pre_Months_Receipts': pre_months_receipt, 
        'Todays_Receipt':todays_receipt,
        'Title' : 'Receipt Dashboard'
        }

    return render(request, 'receipts/dashboard.html', params)


def add_receipt_voucher(request):
    party_data = Sales_Party.objects.all()

    if request.method == 'POST':
        party_GSTIN = Sales_Party.objects.filter(Sales_Con_GSTIN = request.POST.get('Party_GSTIN')).first()
        rcpt_amount = request.POST.get('amount_receive')
        receipt_method = request.POST.get('receipt_method')
        receipt_date = request.POST.get('receipt_date')
        receipt_description = request.POST.get('description')

        add_voucher = Receipt_Voucher(Rcpt_Party_Data=party_GSTIN, Rcpt_Date=receipt_date, Rcpt_Method=receipt_method,Rcpt_Amount=rcpt_amount, Rcpt_Description=receipt_description,)
        add_voucher.save()

    params = {
        'Party_Data': party_data,
        'Title' : 'Receipt Voucher'
    }

    return render(request, 'receipts/index.html', params)


def edit_receipt_voucher(request,v_no):
    voucher_detail = Receipt_Voucher.objects.filter(pk=v_no).first()
    party_data = Sales_Party.objects.all()

    if voucher_detail:
        params = {
            'Voucher_Deatil' : voucher_detail, 
            'Party_Data' :party_data,
            'Title' : 'Edit Receipt Voucher'
            }
        return render(request, 'receipts/edit_voucher.html', params)
    else:
        return redirect('Add_Receipts_Voucher')


def all_receipts_detail(request, type):

    if type == 'total_receipts':
        all_Receipts_Data = Receipt_Voucher.objects.all().order_by('-Rcpt_V_No')
        return render(request, 'receipts/all_receipts.html', {'All_Receipts': all_Receipts_Data, 'Type': type.capitalize, 'Title': f'{type.capitalize().replace('_'," ")}'})
    elif type == 'today_receipts':
        today = timezone.now().date()
        tomorrow = today + timezone.timedelta(days=1)

        all_Receipts_Data = Receipt_Voucher.objects.filter( Rcpt_Date__gte=today, Rcpt_Date__lt=tomorrow).order_by('-Rcpt_V_No')
        return render(request, 'receipts/all_receipts.html', {'All_Receipts': all_Receipts_Data, 'Type': type.capitalize, 'Title': f'{type.capitalize().replace('_'," ")}'})
    elif type == 'this_receipts':
        today = timezone.now()
        all_Receipts_Data = Receipt_Voucher.objects.filter(Rcpt_Date__year=today.year,Rcpt_Date__month=today.month).order_by('-Rcpt_V_No')
        return render(request, 'receipts/all_receipts.html', {'All_Receipts': all_Receipts_Data, 'Type': type.capitalize, 'Title': f'{type.capitalize().replace('_'," ")}'})
    
    elif type == 'pre_receipts':
        today = (timezone.now().month -1)
        year = (timezone.now().year)
        all_Receipts_Data = Receipt_Voucher.objects.filter(Rcpt_Date__year=year, Rcpt_Date__month=today).order_by('-Rcpt_V_No')
        return render(request, 'receipts/all_receipts.html', {'All_Receipts': all_Receipts_Data, 'Type': type.capitalize, 'Title': f'{type.capitalize().replace('_'," ")}'})
    else:
        return redirect('Receipt_Index')

    
def update_receipt_voucher(request):
    if request.method == 'POST':
        party_GSTIN = Sales_Party.objects.filter(Sales_Con_GSTIN = request.POST.get('Party_GSTIN')).first()
        receive_Amount = request.POST.get('amount_receive')
        receive_Method = request.POST.get('receipt_method')
        receive_Date = request.POST.get('receipt_date')
        receive_Description = request.POST.get('description')
        receive_v_no = Receipt_Voucher.objects.filter(Rcpt_V_No=request.POST.get('receive_v_no')).first()

        receive_v_no.Rcpt_Party_Data = party_GSTIN
        receive_v_no.Rcpt_Amount = receive_Amount
        receive_v_no.Rcpt_Method = receive_Method
        receive_v_no.Rcpt_Date = receive_Date
        receive_v_no.Rcpt_Description = receive_Description

        receive_v_no.save()

    return redirect('Receipt_Index')