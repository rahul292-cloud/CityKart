from django.urls import path
from .views import *
from .storeViews import *

urlpatterns = [
    path('AdminLogin/', AdminLogin.as_view()),
    # path('CreateVendorManagement/', CreateVendorManagement.as_view()),
    path('GetAllvendorsDetails/', GetAllvendorsDetails.as_view()),
    path('GetAllvendorsDetails/<str:pk>/', GetAllvendorsDetails.as_view()),
    # path('AddVendorStoreDetails/', AddVendorStoreDetails.as_view()),
    # path('UpdateVendorStoreDetails/', UpdateVendorStoreDetails.as_view()),
    # path('AllVendorStoreDetails/', AllVendorStoreDetails.as_view()),
    # path('getStoreDetailsById/', getStoreDetailsById.as_view()),

    path('productDetailsView/', productDetailsView.as_view()),
    path('productDetailsView/<str:pk>/', productDetailsView.as_view()),

    path('ProductCategoryDetails/', ProductCategoryDetails.as_view()),
    path('ProductCategoryDetails/<str:pk>/', ProductCategoryDetails.as_view()),

    path('SubCategoryDetails/', SubCategoryDetails.as_view()),
    path('SubCategoryDetails/<str:pk>/', SubCategoryDetails.as_view()),

    path('PinCodeDetails/', PinCodeDetails.as_view()),
    path('PinCodeDetails/<str:pk>/', PinCodeDetails.as_view()),

    path('AddProductsToVendor/', AddProductsToVendor.as_view()),
    path('AddProductsToVendor/<str:pk>/', AddProductsToVendor.as_view()),

    path('GetAllProductsForStoreById/', GetAllProductsForStoreById.as_view()),

    # store details
    path('CreateVendorManagementAndStoreDetails/', CreateVendorManagementAndStoreDetails.as_view()),
    path('RegisterVendorDetailsView/', RegisterVendorDetailsView.as_view()),

    path('VendorStoreLogin/', VendorStoreLogin.as_view()),

    path('GetVendorsRegDetails/', GetVendorsRegDetails.as_view()),
    path('GetVendorsRegDetails/<str:pk>/', GetVendorsRegDetails.as_view()),
]