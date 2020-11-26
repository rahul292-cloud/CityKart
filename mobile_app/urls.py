from django.urls import path
from .views import *

urlpatterns = [
    path('AdminLogin/', AdminLogin.as_view()),
    path('CreateVendorManagement/', CreateVendorManagement.as_view()),
    path('GetAllvendorsDetails/', GetAllvendorsDetails.as_view()),
    path('GetAllvendorsDetails/<str:pk>/', GetAllvendorsDetails.as_view()),
    path('AddVendorStoreDetails/', AddVendorStoreDetails.as_view()),
    path('UpdateVendorStoreDetails/', UpdateVendorStoreDetails.as_view()),
    path('AllVendorStoreDetails/', AllVendorStoreDetails.as_view()),
    path('getStoreDetailsById/', getStoreDetailsById.as_view()),
]