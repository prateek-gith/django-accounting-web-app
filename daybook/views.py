from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date
from django.db.models import Value, CharField, F


# Import Models
from purchase.models import Purchase_Voucher
from sales.models import Sales_Party, Sales_Voucher
from payments.models import Payment_Voucher
from receipts.models import Receipt_Voucher

# Create your views here.


from datetime import datetime

def dashboard(request):
    # first try to get date from UI if not found then use date.today().isoformat()
    selected_date = request.GET.get('date', date.today().isoformat())
    total_credit = 0
    total_debit = 0
    if selected_date:
        # convert a string into datetime and '.date()' copy only date part
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()

        # first we filter based on model date with date which is fetch from UI
        # annotate(.....) give us to current time changement on databse column or give a alternet name for current or UI render 
        purchases_detail = Purchase_Voucher.objects.filter(Purchase_Date__date = date_obj).annotate(
            entry_type=Value('Purchase', output_field=CharField()),
            date_field=F('Purchase_Date'),
            v_no=F('Purchase_V_No'),
            amount=F('Purchase_To_Amount')
        ).values('date_field', 'v_no', 'amount', 'entry_type')

        sale_detail = Sales_Voucher.objects.filter(Sale_Date__date = date_obj).annotate(
            entry_type=Value('Sale', output_field=CharField()),
            date_field=F('Sale_Date'),
            v_no=F('Sales_V_No'),
            amount=F('Sale_To_Amount')
        ).values('date_field', 'v_no', 'amount', 'entry_type')

        payment_detail = Payment_Voucher.objects.filter(Pay_Date__date = date_obj).annotate(
            entry_type=Value('Payment', output_field=CharField()),
            date_field=F('Pay_Date'),
            v_no=F('Pay_V_No'),
            amount=F('Pay_Amount')
        ).values('date_field', 'v_no', 'amount', 'entry_type')

        receipt_detail = Receipt_Voucher.objects.filter(Rcpt_Date__date = date_obj).annotate(
            entry_type=Value('Receipts', output_field=CharField()),
            date_field=F('Rcpt_Date'),
            v_no=F('Rcpt_V_No'),
            amount=F('Rcpt_Amount')
        ).values('date_field', 'v_no', 'amount', 'entry_type')

        # convert queryset into a list with concatinate

        day_data = list(sale_detail) + list(purchases_detail) + list(payment_detail) + list(receipt_detail)


        # add credit debit amount for UI render
        for data in day_data:
            if (data['entry_type'] == 'Purchase') or (data['entry_type'] == 'Receipts'):
                total_credit = total_credit + data['amount']
                # print('Total_Credit',total_credit)
            elif (data['entry_type'] == 'Sale') or (data['entry_type'] == 'Payment'):
                total_debit = total_debit + data['amount']
                # print('Total_Debit', total_debit)
            else:
                continue

        params = {
            'Day_Data' : day_data,
            'Total_Credit' : total_credit,
            'Total_Debit' : total_debit,
            'Title' : 'Day Book',
        }

        # we can pass the params whis is a dict, we can directly use parmas key as a variable in UI
        return render(request, 'daybook/daybook.html', params)

    params = {
        'Day_Data' : [],
        'Total_Credit' : total_credit,
        'Total_Debit' : total_debit,
        'Title' : 'Day Book',
    }
    
    return render(request, 'daybook/daybook.html', params)