from django.db import models
import datetime
import random, string

class PinCodeList(models.Model):
    pin_code = models.IntegerField(default=0)
    area = models.CharField(null=False, blank=True, max_length=200)
    region = models.CharField(null=True, blank=True, max_length=200)
    city_name = models.CharField(null=True, blank=True, max_length=200)
    state = models.CharField(null=True, blank=True, max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pin_code)
