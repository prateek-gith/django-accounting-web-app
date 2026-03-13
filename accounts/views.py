from django.shortcuts import render, redirect

# Create your views here.

from sales.models import Sales_Party


def index(request):
    party_data = Sales_Party.objects.all()

    if request.method == 'POST':
        party_GSTIN = request.POST.get('gstin')
        party_name = request.POST.get('name')
        party_address = request.POST.get('address')
        party_pincode = request.POST.get('pincode')

        add_party = Sales_Party(Sales_Con_GSTIN = party_GSTIN , Sales_Con_Name = party_name, Sales_Con_Address = party_address , Sales_Con_Pincode = party_pincode)
        add_party.save()

    # all_Purchase_Data = Purchase_Voucher.objects.all()
    return render(request, 'accounts/accounta.html', {'Party_Data' : party_data, 'Title': "Add Party"})

def all_parties(request):
    party_data = Sales_Party.objects.all()

    return render(request, 'accounts/dashboard.html', {'Party_Data' : party_data, 'Title': "Account Dashboard"})

def edit_account(request, acc_id):
    party_data = Sales_Party.objects.filter(pk=acc_id).first()
    if party_data:
        return render(request, 'accounts/edit_account.html', {'Party_Data' : party_data})
    else:
        return redirect('Account_Index')
    
def update_account(request):
    if request.method == 'POST':
        party_GSTIN = request.POST.get('gstin')
        party_name = request.POST.get('name')
        party_address = request.POST.get('address')
        party_pincode = request.POST.get('pincode')

        party_detail = Sales_Party.objects.filter(pk=request.POST.get('account_id')).first()

        if party_detail:
            party_detail.Sales_Con_GSTIN = party_GSTIN
            party_detail.Sales_Con_Name = party_name
            party_detail.Sales_Con_Address = party_address
            party_detail.Sales_Con_Pincode = party_pincode
            
            party_detail.save()

    
    return redirect('Account_Index')