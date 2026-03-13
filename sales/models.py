from django.db import models
from django.utils import timezone
# Create your models here.

class Sales_Party(models.Model):
    Sales_Co_ID = models.AutoField(primary_key=True)
    Sales_Con_GSTIN = models.CharField(max_length=15, default="URP", unique=True, null=False)
    Sales_Con_Name = models.CharField(max_length=50, null=False)
    Sales_Con_Address = models.CharField(max_length=200, default="N/A")
    Sales_Con_Pincode = models.IntegerField(default=000000)

    def __str__(self):
        return f"{self.Sales_Con_GSTIN} - {self.Sales_Con_Name}"



class Sales_Voucher(models.Model):
    Sales_V_No = models.AutoField(primary_key=True)
    # Sales_Party_Name = models.CharField(max_length=100)
    # Sale_GSTIN = models.CharField(max_length=15)
    Sales_Party_Data = models.ForeignKey(Sales_Party, on_delete=models.CASCADE, null=True, blank= True)
    Sale_Date = models.DateTimeField(default=timezone.now)
    Sale_Item_Name = models.CharField(max_length=50, default="Item", null=False)
    Sale_Item_Qn = models.FloatField(default=0.00)
    Sale_Item_UOM = models.CharField(max_length=3, default="Pcs.")
    Sale_Item_Rate = models.FloatField(default=0.00)
    Sale_item_To_Value = models.FloatField(default=0.00)
    Sale_GST_Per = models.FloatField(default=0.00)
    Sale_GST_Amount = models.FloatField(default=0.00)
    Sale_To_Amount = models.FloatField(default=0.00)
    

    def __str__(self):
        return f"{self.Sales_V_No} - {self.Sales_Party_Data}"
    
