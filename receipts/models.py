from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from sales.models import Sales_Party

# Create your models here.

class Receipt_Voucher(models.Model):
    Rcpt_V_No = models.AutoField(primary_key=True)
    Rcpt_Party_Data = models.ForeignKey(Sales_Party, on_delete=models.CASCADE, null=True, blank= True)
    Rcpt_Date = models.DateTimeField(default=timezone.now)
    Rcpt_Method = models.CharField(default="Cash")
    Rcpt_Amount = models.FloatField(default=0.00)
    Rcpt_Description = models.TextField(default="")
    

    def __str__(self):
        return f"{self.Rcpt_V_No} - {self.Rcpt_Party_Data}"