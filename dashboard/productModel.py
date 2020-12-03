from django.db import models
import datetime
import random, string


def randomword(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

def randomNo():
    return random.randint(1000,9999)

class Product_category(models.Model):
    category_id = models.IntegerField(null=False, blank=True, default=randomNo)
    category_name = models.CharField(null=False, blank=True, max_length=200)
    category_description = models.CharField(null=True, blank=True, max_length=200)
    product_thumbnail = models.FileField(blank=True, null=True, upload_to='productCategoryImages/')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.category_name


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.created_at = datetime.datetime.now()
            product_category_save = super(Product_category, self).save(force_insert=False, force_update=False,
                                                                       using=None,
                                                                       update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            product_category_save = super(Product_category, self).save(force_insert=False, force_update=False,
                                                                       using=None,
                                                                       update_fields=None)
        return product_category_save


class Product(models.Model):
    product_id = models.CharField(default=randomword(5), null=False, blank=True, max_length=100, unique=True)
    product_category_id = models.ForeignKey(Product_category, on_delete=models.SET_NULL, null=True, blank=True) # models.CASCADE
    product_name = models.CharField(null=False, blank=True, max_length=200)
    product_description = models.CharField(null=True, blank=True, max_length=200)
    product_images = models.FileField(blank=True, null=True, upload_to='productImages/')
    product_price = models.FloatField(default=0.0)
    gst = models.IntegerField(default=0)
    discount = models.FloatField(default=0.0)
    rating = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    subscription = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    trending = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.product_id = randomword(5)
            self.created_at = datetime.datetime.now()
            product_save = super(Product, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            product_save = super(Product, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        return product_save
