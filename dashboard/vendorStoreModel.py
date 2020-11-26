from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
import datetime
from .vendorModel import Vendor_management
import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


class VendorStore(models.Model):
    vendorStore_id = models.CharField(default=randomword(5), null=False, blank=True, max_length=100, unique=True)
    vendor_id = models.ForeignKey(Vendor_management, on_delete=models.SET_NULL, null=True, blank=True)
    store_name = models.CharField(max_length=1000, null=True, blank=True)
    popular_name = models.CharField(max_length=2000, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    post_code = models.CharField(max_length=500, null=True, blank=True)
    contact_person = models.CharField(max_length=1000, null=True, blank=True)
    contact_no1 = models.CharField(max_length=500, null=True, blank=True)
    contact_no2 = models.CharField(max_length=500, null=True, blank=True)
    loc_latitude = models.FloatField(null=True, blank=True)
    loc_lonitude = models.FloatField(null=True, blank=True)


    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk is None:
            self.vendorStore_id = randomword(5)
            self.created_at = datetime.datetime.now()

            res = super(VendorStore, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        else:
            # self.vendorStore_id = randomword(5)
            self.updated_at = datetime.datetime.now()
            res = super(VendorStore, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return res
