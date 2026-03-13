from django.shortcuts import render, redirect
from django.utils import timezone

# my_date = timezone.now()
# print("mydate is",my_date.month)



# Import Models
from .models import Purchase_Voucher
from sales.models import Sales_Party

from django.http import JsonResponse,HttpResponse

from functools import reduce

import os



import requests
from weasyprint import HTML

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# for  rupees ₹ symbol
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics



def sum_data(num_1,num_2):
    # print("num1: ",num_1, "num2",num_2)
    return num_1 + num_2.Purchase_To_Amount
    
def filter_by_date(my_list):
    return my_list.Purchase_Date.month == timezone.now().month

def filter_by_pre_date(my_list):
    return my_list.Purchase_Date.month == (timezone.now().month - 1)

def filter_by_today(my_list):
    return my_list.Purchase_Date.date() == (timezone.now().date())


# Create your views here.

def index(request):
    all_Purchase_Data = Purchase_Voucher.objects.all()
    print(all_Purchase_Data)
    # print([al.Purchase_To_Amount for al in all_Purchase_Data])
    total_Purchase_value = reduce(sum_data, all_Purchase_Data,0)
    this_months_Purchase = reduce(sum_data,list(filter(filter_by_date, all_Purchase_Data)),0 )

    if (list(filter(filter_by_pre_date, all_Purchase_Data))) != []:
        pre_months_Purchase = reduce(sum_data, (list(filter(filter_by_pre_date, all_Purchase_Data))), 0)
    else:
        pre_months_Purchase = 0

    if (list(filter(filter_by_today, all_Purchase_Data))) != []:
        todays_Purchase = reduce(sum_data, list(filter(filter_by_today, all_Purchase_Data)), 0)
    else:
        todays_Purchase = 0


    # todays_Purchase = reduce(sum_data, list(filter(filter_by_today, all_Purchase_Data)) )
    return render(request, 'purchase/dashboard.html', {'Purchase_Data' : all_Purchase_Data, 'Total_Purchase' : total_Purchase_value, "This_Months_Purchase" : this_months_Purchase, 'Previous_Months_Purchase':pre_months_Purchase, 'Todays_Purchase': todays_Purchase,'Title':'Purchase Dashboard', 'Title' : 'Purchase Dashboard'})


def add_Purchase_voucher(request):
    party_data = Sales_Party.objects.all()

    if request.method == 'POST':
        party_GSTIN = Sales_Party.objects.filter(Sales_Con_GSTIN = request.POST.get('Party_GSTIN')).first()
        item_name = request.POST.get('Item_Name')
        quantity = request.POST.get('Quantity')
        umo = request.POST.get('UOM')
        rate = request.POST.get('Rate')
        to_value = request.POST.get('To_Value')
        gst_per = request.POST.get('GST_Per')
        gst_amount = request.POST.get('GST_Amount')
        sub_total = request.POST.get('Sub_Total')

        add_voucher = Purchase_Voucher(Purchase_Party=party_GSTIN, Purchase_Item_Name=item_name, Purchase_Item_Qn=quantity,Purchase_Item_UOM=umo, Purchase_Item_Rate=rate,Purchase_item_To_Value=to_value , Purchase_GST_Per= gst_per,Purchase_GST_Amount=gst_amount, Purchase_To_Amount = sub_total)
        add_voucher.save()

    # all_Purchase_Data = Purchase_Voucher.objects.all()
    return render(request, 'purchase/purchase_voucher.html', {'Party_Data' : party_data, 'Title': "Purchase Voucher"})

def get_party_details(request, GSTIN):
    gstin = GSTIN
    try:
        party = Sales_Party.objects.get(Sales_Con_GSTIN=gstin)
        data = {
            'name': party.Sales_Con_Name,
            'address': party.Sales_Con_Address,
            'pincode': party.Sales_Con_Pincode,
        }
    except Sales_Party.DoesNotExist:
        data = {'error': 'Party not found'}
    return JsonResponse(data)


def all_Purchase_detail(request, type):

    if type == 'total_purchase':
        all_Purchase_Data = Purchase_Voucher.objects.all().order_by('-Purchase_V_No')
        return render(request, 'purchase/all_purchase_data.html', {'All_Purchase': all_Purchase_Data, 'Type': type.capitalize, 'Title':'Purchase Register'})
    elif type == 'today_purchase':
        today = timezone.now().date()
        tomorrow = today + timezone.timedelta(days=1)

        all_Purchase_Data = Purchase_Voucher.objects.filter( Purchase_Date__gte=today, Purchase_Date__lt=tomorrow).order_by('-Purchase_V_No')
        return render(request, 'purchase/all_purchase_data.html', {'All_Purchase': all_Purchase_Data, 'Type': type.capitalize,'Title':'Purchase Register'})
    elif type == 'this_month':
        today = timezone.now()
        all_Purchase_Data = Purchase_Voucher.objects.filter(Purchase_Date__year=today.year,Purchase_Date__month=today.month).order_by('-Purchase_V_No')
        return render(request, 'purchase/all_purchase_data.html', {'All_Purchase': all_Purchase_Data, 'Type': type.capitalize,'Title':'Purchase Register'})
    
    elif type == 'pre_month':
        today = (timezone.now().month -1)
        year = (timezone.now().year)
        all_Purchase_Data = Purchase_Voucher.objects.filter(Purchase_Date__year=year, Purchase_Date__month=today).order_by('-Purchase_V_No')
        return render(request, 'purchase/all_purchase_data.html', {'All_Purchase': all_Purchase_Data, 'Type': type.capitalize,'Title':'Purchase Register'})
    else:
        return redirect('Purchase_Index')


def edit_voucher(request, v_no):
    v_no_n = v_no
    if v_no_n:
        detail_v_no = Purchase_Voucher.objects.filter(Purchase_V_No=v_no_n).first()
        return render(request , 'purchase/edit_detail.html',{'Voucher_Detail' : detail_v_no, 'Title':'Edit Purchase Voucher'})
    else:
        return redirect('Purchase_Index')
    
def update_purchase_voucher(request):
    if request.method == 'POST':
        party_GSTIN = Sales_Party.objects.filter(Sales_Con_GSTIN = request.POST.get('Party_GSTIN')).first()
        v_Date = request.POST.get('v_date')
        item_name = request.POST.get('Item_Name')
        quantity = request.POST.get('Quantity')
        uom = request.POST.get('UOM')
        rate = request.POST.get('Rate')
        to_value = request.POST.get('To_Value')
        gst_per = request.POST.get('GST_Per')
        gst_amount = request.POST.get('GST_Amount')
        sub_total = request.POST.get('Sub_Total')
        detail_v_no = Purchase_Voucher.objects.filter(Purchase_V_No=request.POST.get('v_no')).first()

        # update According to V_No
        detail_v_no.Purchase_Party=party_GSTIN
        detail_v_no.Purchase_Date=v_Date
        detail_v_no.Purchase_Item_Name=item_name
        detail_v_no.Purchase_Item_Qn=quantity
        detail_v_no.Purchase_Item_UOM=uom
        detail_v_no.Purchase_Item_Rate=rate
        detail_v_no.Purchase_item_To_Value=to_value
        detail_v_no.Purchase_GST_Per=gst_per
        detail_v_no.Purchase_GST_Amount=gst_amount
        detail_v_no.Purchase_To_Amount=sub_total

        detail_v_no.save()

    return redirect('Purchase_Index')


def pdf_gen(request, v_no):

    detail_v_no = Purchase_Voucher.objects.filter(Purchase_V_No=v_no).first()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"attachment; filename={v_no}_bill.pdf "
    
    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # Path to company logo (ensure the path is correct)
    # logo_path = os.path.join(r"C:\Users\hp\Desktop\Django (Projects)\florance\myapp\static\myapp\images\logo\logo.png")  # Update this path as per your project structure

    # Add Company Logo (if available)
    try:
        # c.drawImage(logo_path, width / 2 - 50, height - 80, width=100, height=50, preserveAspectRatio=True, mask='auto')
        
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 90, "COMPANY NAME")
        
        c.setFont("Helvetica-Bold", 15)
        c.drawCentredString(width / 2, height - 110, "ADDRESS")
    except Exception as e:
        print("Error loading logo:", e)

        # Company Name (Centered Below Logo)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(width / 2, height - 120, "FloSun Flower Pvt. Ltd. ")

    # Bill Details
    c.setFont("Helvetica-Bold", 12)
    y_position = height - 140
    c.drawCentredString(width / 2, y_position, "Purchase Invoice")
    
    y_position = height - 160
    c.drawString(50, y_position, f"Sale V No : PVN/0{v_no}")
    
    date=detail_v_no.Purchase_Date.strftime("%d-%b-%Y %I:%M %p")

    c.drawString(355, y_position, f"Date : {date}")

    y_position -= 15

    c.drawString(50, y_position, f"Bill To")
    c.drawString(50, y_position-15, f"Party Name : {detail_v_no.Purchase_Party.Sales_Con_Name}")
    c.drawString(50, y_position-30, f"Party GSTIN : {detail_v_no.Purchase_Party.Sales_Con_GSTIN}")
    c.drawString(50, y_position-45, f"Party Add. : {detail_v_no.Purchase_Party.Sales_Con_Address}")
    c.drawString(50, y_position-60, f"Party Add. : {detail_v_no.Purchase_Party.Sales_Con_Pincode}")
    
    y_position -= 65


    # Table Header
    data = [["Product Name", "Quantity", "Amount", "Total"]]
    
    # Add Item Details
    data.append([f"{detail_v_no.Purchase_Item_Name}",f"{detail_v_no.Purchase_Item_Qn}/{detail_v_no.Purchase_Item_UOM}", f"{detail_v_no.Purchase_Item_Rate}",f"{detail_v_no.Purchase_item_To_Value}"])

    # Add Subtotal Row
    data.append(["Subtotal", f"{detail_v_no.Purchase_Item_Qn}/{detail_v_no.Purchase_Item_UOM}", "", f"{detail_v_no.Purchase_item_To_Value}"])
    
    # Add GST Details
    data.append(["", "", f"GST @{detail_v_no.Purchase_GST_Per}%", f"{detail_v_no.Purchase_GST_Amount}"])
    data.append(["", "", "Invoice Vale", f"{detail_v_no.Purchase_To_Amount}"])


    # Create Table
    table = Table(data, colWidths=[200, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 50, y_position - len(data) * 20)

    # Shipping Address
    y_position -= (len(data) + 2) * 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Shipping Address:")
    y_position -= 20

    c.setFont("Helvetica", 10)
    # buyer_name=all_pur_products.Place_Order_User_Name
    # buyer_address=all_pur_products.Place_Order_Address[0]['address']
    # buyer_district=all_pur_products.Place_Order_Address[0]['city']
    # buyer_state = all_pur_products.Place_Order_Address[0]['state']
    # buyer_mobile = all_pur_products.Place_Order_Address[0]['mobile_no']
    # buyer_pincode = all_pur_products.Place_Order_Address[0]['pincode']
    # c.drawString(50, y_position, f"Buyer Name: {buyer_name}")
    # c.drawString(50, y_position - 20, f"Address: {buyer_address}")
    # c.drawString(50, y_position - 40, f"State: {buyer_state}, District: {buyer_district}, Pin Code : {buyer_pincode}")
    # c.drawString(50, y_position - 60, f"Mobile Number: {buyer_mobile}")

    # Save PDF
    c.showPage()
    c.save()

    return response
    # return HttpResponse("<h1> Shree Ram </h1>")



