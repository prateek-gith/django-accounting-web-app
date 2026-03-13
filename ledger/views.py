from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date
# from django.db.models import F
from django.db.models import Value, CharField, F




# Import Models
from purchase.models import Purchase_Voucher
from sales.models import Sales_Party, Sales_Voucher
from payments.models import Payment_Voucher
from receipts.models import Receipt_Voucher

# from django.http import JsonResponse

# from functools import reduce



# Create your views here.

def index(request):
    selected_party_id = request.GET.get('party_id')
    party = None
    ledger_data = []
    total_sale = 0
    total_purchase = 0
    total_payments = 0
    total_receipts = 0

    if selected_party_id:
        party = Sales_Party.objects.get(pk=selected_party_id)

        # Sales entries (Credit)
        sales = Sales_Voucher.objects.filter(Sales_Party_Data=party).annotate(
            entry_type=Value('Sale', output_field=CharField()),
            date_field=F('Sale_Date'),
            v_no=F('Sales_V_No'),
            amount=F('Sale_To_Amount')
        ).values('date_field', 'v_no', 'amount', 'entry_type')

        # Purchase entries (Debit)
        purchases = Purchase_Voucher.objects.filter(Purchase_Party=party).annotate(
            entry_type=Value('Purchase', output_field=CharField()),
            date_field=F('Purchase_Date'),
            v_no=F('Purchase_V_No'),
            amount=F('Purchase_To_Amount')
        ).values('date_field', 'v_no', 'amount', 'entry_type')

        # Payment entries (Debit)
        payments = Payment_Voucher.objects.filter(Pay_Party_Data=party).annotate(
            entry_type=Value('Payment', output_field=CharField()),
            date_field=F('Pay_Date'),
            v_no=F('Pay_V_No'),
            amount=F('Pay_Amount')
        ).values('date_field', 'v_no', 'amount', 'entry_type')

        # Payment entries (Debit)
        receipts = Receipt_Voucher.objects.filter(Rcpt_Party_Data=party).annotate(
            entry_type=Value('Receipts', output_field=CharField()),
            date_field=F('Rcpt_Date'),
            v_no=F('Rcpt_V_No'),
            amount=F('Rcpt_Amount')
        ).values('date_field', 'v_no', 'amount', 'entry_type')

        # Combine and sort by date
        ledger_data = list(sales) + list(purchases) + list(payments) + list(receipts)
        # print(ledger_data)
        ledger_data = sorted(ledger_data, key=lambda x: x['date_field'])

        # Calculate running balance
        balance = 0
        for entry in ledger_data:
            if entry['entry_type'] == 'Sale' or entry['entry_type'] == 'Payment':
                balance += float(entry['amount'])   # credit
            else:
                balance -= float(entry['amount'])   # debit
            entry['balance'] = balance

        for to_sl in ledger_data:
            if to_sl['entry_type'] ==  'Sale':
                total_sale = total_sale + to_sl['amount']
            elif to_sl['entry_type'] == 'Purchase':
                total_purchase = total_purchase + to_sl['amount']
            elif to_sl['entry_type'] == 'Payment':
               total_payments =total_payments + to_sl['amount']
            elif to_sl['entry_type'] == 'Receipts':
               total_receipts =total_receipts + to_sl['amount']
            else:
                continue
        
        # print(ledger_data)
    

    context = {
        'parties': Sales_Party.objects.all(),
        'party': party,
        'ledger_data': ledger_data,
        'Total_Sale' : total_sale,
        'Total_Pruchase' : total_purchase,
        'Total_Payments' : total_payments,
        'Total_Receipts' : total_receipts,
        'Title' : 'Leadger Dashboard'
    }

    
    return render(request, 'ledger/ledger_dashboard.html', context)

