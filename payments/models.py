from django.db import models
from django.utils import timezone
from sales.models import Sales_Party

# Create your models here.

class Payment_Voucher(models.Model):
    Pay_V_No = models.AutoField(primary_key=True)
    Pay_Party_Data = models.ForeignKey(Sales_Party, on_delete=models.CASCADE, null=True, blank= True)
    Pay_Date = models.DateTimeField(default=timezone.now)
    Pay_Method = models.CharField(default="Cash")
    Pay_Amount = models.FloatField(default=0.00)
    Pay_Description = models.TextField(default="")
    

    def __str__(self):
        return f"{self.Pay_V_No} - {self.Pay_Party_Data}"