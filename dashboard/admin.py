from django.contrib import admin

from .vendorModel import Vendor_management
from .vendorStoreModel import VendorStore
from .vendorStockModel import Vendor_Stock

admin.site.register(Vendor_management)
admin.site.register(VendorStore)
admin.site.register(Vendor_Stock)
