from django.db import models
from django.utils import timezone

from sales.models import Sales_Party
# Create your models here.

class Purchase_Voucher(models.Model):
    Purchase_V_No = models.AutoField(primary_key=True)
    # Purchase_Party_Name = models.CharField(max_length=100)
    # Purchase_GSTIN = models.CharField(max_length=15)
    Purchase_Party = models.ForeignKey(Sales_Party, on_delete=models.CASCADE, null=True, blank= True)
    Purchase_Date = models.DateTimeField(default=timezone.now)
    Purchase_Item_Name = models.CharField(max_length=50, default="Item", null=False)
    Purchase_Item_Qn = models.FloatField(default=0.00)
    Purchase_Item_UOM = models.CharField(max_length=3, default="Pcs.")
    Purchase_Item_Rate = models.FloatField(default=0.00)
    Purchase_item_To_Value = models.FloatField(default=0.00)
    Purchase_GST_Per = models.FloatField(default=0.00)
    Purchase_GST_Amount = models.FloatField(default=0.00)
    Purchase_To_Amount = models.FloatField(default=0.00)
    

    def __str__(self):
        return f"{self.Purchase_V_No} - {self.Purchase_Party}"
    
