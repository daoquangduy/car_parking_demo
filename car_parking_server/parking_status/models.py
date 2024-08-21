from django.db import models

# Create your models here.
class Data(models.Model):
    parkingName = models.CharField(max_length=200)
    freeSlots = models.CharField(max_length=500)
    updateTime = models.DateTimeField(auto_now_add=True)