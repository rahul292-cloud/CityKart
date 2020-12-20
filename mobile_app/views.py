from django.shortcuts import render
from django.db.models import (Case, CharField, Count, DateTimeField,
                              ExpressionWrapper, F, FloatField, Func, Max, Min,
                              Prefetch, Q, Sum, Value, When, Subquery)

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status, viewsets
from django.http import Http404
from django.contrib.auth.models import User
import random
import re
from dashboard.vendorModel import Vendor_management
from dashboard.vendorStoreModel import VendorStore
from dashboard.productModel import Product, Product_category
from dashboard.vendorStockModel import Vendor_Stock

from .serializers import *


# Admin Login or super user login
class AdminLogin(ObtainAuthToken):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            password = serializer.validated_data['password']

            token, created = Token.objects.get_or_create(user=user)

            if token.user.is_superuser:
                return Response({"token":token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"msg":"invalid User !"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# sign up vender register   --- used by admin site
# class CreateVendorManagement(CreateAPIView):
#     model = Vendor_management
#     permission_classes = (AllowAny,)
#     serializer_class = VendorManagementSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = VendorManagementSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"data":serializer.data}, status=status.HTTP_200_OK)
#
#         return Response({"msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# get all vendors details  ... admin site
class GetAllvendorsDetails(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk=None):
        if pk:
            response = "Vendors Not Available"
            pk = pk

            data = Vendor_management.objects.filter(id=pk)
            serializer = GetVendorManagementSerializer(data, many=True)
            if data:
                response = serializer.data
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = "Vendors Not Available"

            data = Vendor_management.objects.all().order_by('-pk')
            serializer = GetVendorManagementSerializer(data, many=True)
            if data:
                response = serializer.data
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# # add vendor store details by vendor id .... only for admin
# class AddVendorStoreDetails(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         vendor_id = request.data.get('vendor_id', False)
#         store_name = request.data.get('store_name', False)
#         popular_name = request.data.get('popular_name', False)
#         address = request.data.get('address', False)
#         city = request.data.get('city', False)
#         post_code = request.data.get('post_code', False)
#         contact_person = request.data.get('contact_person', False)
#         contact_no1 = request.data.get('contact_no1', False)
#         contact_no2 = request.data.get('contact_no2', False)
#
#         V_store = VendorStore.objects.filter(vendor_id__vendor_id=vendor_id)
#         if V_store.exists():
#             return Response({"msg":"Already Added this details , You Can Update!"}, status=status.HTTP_400_BAD_REQUEST)
#
#         v_store = VendorStore.objects.create(vendor_id=Vendor_management.objects.get(vendor_id=vendor_id),
#                                             store_name=store_name,
#                                             popular_name=popular_name,
#                                             address=address, city=city,
#                                             post_code=post_code,
#                                             contact_person=contact_person,
#                                             contact_no1=contact_no1,
#                                             contact_no2=contact_no2)
#         if v_store:
#             return Response({"data":"Details Added Successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"msg":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

# update vendor store details by vendor id .... only for admin
# class UpdateVendorStoreDetails(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         vendor_id = request.data.get('vendor_id', False)
#         store_name = request.data.get('store_name', False)
#         popular_name = request.data.get('popular_name', False)
#         address = request.data.get('address', False)
#         city = request.data.get('city', False)
#         post_code = request.data.get('post_code', False)
#         contact_person = request.data.get('contact_person', False)
#         contact_no1 = request.data.get('contact_no1', False)
#         contact_no2 = request.data.get('contact_no2', False)
#
#         v_store = VendorStore.objects.filter(vendor_id__vendor_id=vendor_id).update(store_name=store_name, popular_name=popular_name,
#                                                                                     address=address, city=city, post_code=post_code,
#                                                                                     contact_person=contact_person, contact_no1=contact_no1,
#                                                                                     contact_no2=contact_no2)
#         if v_store:
#             return Response({"data":"Details Updated Successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"msg":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


# Store Details:  -- admin panel
# class AllVendorStoreDetails(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         allVendorStore = VendorStore.objects.all().values('id', 'vendorStore_id', 'store_name',
#                                                           'popular_name', 'address', 'city', 'post_code',
#                                                           'contact_person', 'contact_no1', 'contact_no2',
#                                                           'loc_latitude', 'loc_lonitude', 'created_at',
#                                                           'updated_at').annotate(
#             vendor_Id=F('vendor_id__vendor_id'),
#             vendor_userName=F('vendor_id__userName'),
#             # vendor_password=F('vendor_id__password'),
#             vendor_first_name=F('vendor_id__first_name'),
#             vendor_last_name=F('vendor_id__last_name'),
#             vendor_table_id=F('vendor_id__id'),
#         ).order_by('-pk')
#
#         if allVendorStore:
#             return Response({"data":allVendorStore}, status=status.HTTP_200_OK)
#         else:
#             return Response({"msg":"Something went wrong!"}, status=status.HTTP_400_BAD_REQUEST)


# # get store details by Id   .... for admin site  .. delivery made cancel
# class getStoreDetailsById(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, pk=None):
#         vendor_id = request.data.get('vendor_id', False)
#
#         vendor_store_details = VendorStore.objects.filter(vendor_id__vendor_id=vendor_id).values('id', 'vendorStore_id',
#                                                                                                  'store_name', 'popular_name',
#                                                                                                  'address', 'city', 'post_code',
#                                                                                                  'contact_person', 'contact_no1',
#                                                                                                  'contact_no2', 'created_at').annotate(
#             vendor_userName = F('vendor_id__userName'),
#             vendor_password = F('vendor_id__password'),
#         )
#         if vendor_store_details.exists():
#             return Response({"data":vendor_store_details[0]}, status=status.HTTP_200_OK)
#         else:
#             return Response({"msg":"Store Details Is not Available , Add Store !"}, status=status.HTTP_400_BAD_REQUEST)


# get or create product category
class ProductCategoryDetails(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            pk = pk
            return Product_category.objects.get(pk=pk)
        except Product_category.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            response = []
            pk = pk

            data = Product_category.objects.filter(id=pk)
            serializer = Product_CategorySerializer(data, many=True)
            if data:
                response = serializer.data
            return Response(response)

        else:
            response = []
            pk = None
            data = Product_category.objects.all().order_by('-pk')
            serializer = Product_CategorySerializer(data, many=True)
            if data:
                response = serializer.data
            return Response(response)

    def post(self, request, pk=None):
        print(request.data)

        serializer = Product_CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = Product_CategorySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # pk = ObjectId(pk)
        pk = pk
        productCategory = self.get_object(pk)
        productCategory.delete()
        return Response("productCategory Deleted")


# get or create the product
class productDetailsView(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            pk = pk
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        print(request.data)
        if pk:
            response = []
            pk = pk

            data = Product.objects.filter(id=pk)
            serializer = Product_viewSerializer(data, many=True)
            if data:
                response = serializer.data
            return Response(response)

        else:
            response = []
            pk = None

            data = Product.objects.all().order_by('-pk')
            print(data)
            serializer = Product_viewSerializer(data, many=True)
            if data:
                response = serializer.data
            return Response(response)

    def post(self, request, pk=None):
        print(request.data)

        serializer = Product_viewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # pk = ObjectId(pk)
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = Product_viewSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # pk = ObjectId(pk)
        pk = pk
        product = self.get_object(pk)
        product.delete()
        return Response("product Deleted")

# create vendor stock ...admin can only create
# add products to vendor store ... only for admin
# asign products to vendors
class AddProductsToVendor(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            pk = pk
            return Vendor_Stock.objects.get(pk=pk)
        except Vendor_Stock.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        vendor_id = request.data.get('vendor_id', False)
        product_id = request.data.get('product_id', False)
        vendor_Stock = Vendor_Stock.objects.filter(vendor_id__id=vendor_id, product_id=product_id)
        if vendor_Stock.exists():
            return Response('This Product Is Already Exists !', status=status.HTTP_400_BAD_REQUEST)

        serializer = AddProductsToVendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            product_category = Product.objects.filter(id=serializer.data['product_id']).values('id').annotate(product_categoryId = F('product_category_id__id'))
            # print(product_category)
            # print(product_category[0]['product_categoryId'])
            try:
                Vendor_Stock.objects.filter(id=serializer.data['id']).update(product_category_id=Product_category.objects.get(id=product_category[0]['product_categoryId']))
            except:
                product = self.get_object(serializer.data['id'])
                product.delete()
                return Response("Something went wrong ", status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # pk = ObjectId(pk)
        print(request.data)
        id = pk
        instance = self.get_object(id)

        serializer = AddProductsToVendorSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pk = pk
        product = self.get_object(pk)
        product.delete()
        return Response("Item Deleted ", status=status.HTTP_200_OK)

# get stock details by vendor id .... admin only
class GetAllProductsForStoreById(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        vendor_id = request.data.get('vendor_id', False)

        v_stock = Vendor_Stock.objects.filter(vendor_id__vendor_id=vendor_id).values('id', 'quantity').annotate(
            product_product_id = F('product_id__product_id'),
            product_product_name = F('product_id__product_name'),
            product_product_description = F('product_id__product_description'),
            product_product_images = F('product_id__product_images'),
            product_product_price = F('product_id__product_price'),
            product_gst = F('product_id__gst'),
            product_product_status = F('product_id__product_status'),
            product_discount = F('product_id__discount'),
            product_rating = F('product_id__rating'),
            product_subscription = F('product_id__subscription'),

            product_category_category_id = F('product_category_id__category_id'),
            product_category_category_name = F('product_category_id__category_name'),
            product_category_category_description = F('product_category_id__category_description'),
            product_category_product_thumbnail = F('product_category_id__product_thumbnail'),
        )
        if v_stock:
            return Response(v_stock, status=status.HTTP_200_OK)
        else:
            return Response("Products are not available", status=status.HTTP_400_BAD_REQUEST)



