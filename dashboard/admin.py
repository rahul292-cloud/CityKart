from django.contrib import admin

from .vendorModel import Vendor_management
from .vendorStoreModel import VendorStore
from .vendorStockModel import Vendor_Stock
from .productModel import Product_category, Product

admin.site.register(Vendor_management)
admin.site.register(VendorStore)
admin.site.register(Vendor_Stock)
admin.site.register(Product_category)
admin.site.register(Product)
