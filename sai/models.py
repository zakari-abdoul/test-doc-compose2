from django.db import models

# '%b %d, %Y',      # 'Oct 25, 2006'


class Sai_IN(models.Model):
    Interval_Time = models.CharField(max_length=25)
    PLMN_Carrier = models.CharField(max_length=100)
    Direction = models.CharField(max_length=40)
    Service = models.CharField(max_length=20)
    Opcode = models.CharField(max_length=100)
    HVA = models.CharField(max_length=40)
    Total_Transactions = models.PositiveIntegerField()
    Failed_Transactions =models.PositiveIntegerField()
    EFF =  models.PositiveIntegerField()
    
    def __str__(self):
        return "SAI_IN"


class Sai_OUT(models.Model):
    Interval_Time = models.CharField(max_length=25)
    PLMN_Carrier = models.CharField(max_length=100)
    Direction = models.CharField(max_length=40)
    Service = models.CharField(max_length=20)
    Opcode = models.CharField(max_length=100)
    HVA = models.CharField(max_length=40)
    Total_Transactions = models.PositiveIntegerField()
    Failed_Transactions =models.PositiveIntegerField()
    EFF =  models.PositiveIntegerField()
    
    def __str__(self):
        return "Sai_OUT"