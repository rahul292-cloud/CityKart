from django.db import models
from django.core.validators import RegexValidator
import datetime
from .vendorModel import Vendor_management
# from .productModel import Product, Product_category

class Vendor_Stock(models.Model):
    vendor_id = models.ForeignKey(Vendor_management, on_delete=models.SET_NULL, null=True, blank=True)
    # product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    # product_category_id = models.ForeignKey(Product_category, on_delete=models.SET_NULL, null=True, blank=True)
    quantity =  models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    selling_price = models.FloatField(default=0.0)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk is None:
            self.created_at = datetime.datetime.now()

            res = super(Vendor_Stock, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            res = super(Vendor_Stock, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return res