from django.db import models
from asset.models import *

# Create your models here.

#Service Requests model
class Requested(models.Model):
    request_pk = models.AutoField(primary_key=True)
    request_number = models.CharField(max_length=40, null=False)
    request_service = models.CharField(max_length=40, null=False)
    request_reason = models.CharField(max_length=100, null=False)
    request_date = models.DateField(auto_now_add=True)
    comp = models.ForeignKey(Comp, null=True, on_delete=models.SET_NULL)
