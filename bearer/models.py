from django.db import models



class Bearer(models.Model):
    Type = models.CharField(max_length=20)
    Interval_Time = models.CharField(max_length=20)
    PLMN_Carrier = models.CharField(max_length=100)
    Direction = models.CharField(max_length=40)
    Service = models.CharField(max_length=20)
    Opcode = models.CharField(max_length=100)
    HVA = models.CharField(max_length=40)
    Total_Transactions = models.PositiveIntegerField()
    Failed_Transactions =models.PositiveIntegerField()
    EFF =  models.PositiveIntegerField()
    
    def __str__(self):
        return self.Service