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
class CreateVendorManagement(CreateAPIView):
    model = Vendor_management
    permission_classes = (AllowAny,)
    serializer_class = VendorManagementSerializer

    def post(self, request, *args, **kwargs):
        serializer = VendorManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)

        return Response({"msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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


# add vendor store details by vendor id .... only for admin
class AddVendorStoreDetails(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        vendor_id = request.data.get('vendor_id', False)
        store_name = request.data.get('store_name', False)
        popular_name = request.data.get('popular_name', False)
        address = request.data.get('address', False)
        city = request.data.get('city', False)
        post_code = request.data.get('post_code', False)
        contact_person = request.data.get('contact_person', False)
        contact_no1 = request.data.get('contact_no1', False)
        contact_no2 = request.data.get('contact_no2', False)

        V_store = VendorStore.objects.filter(vendor_id__vendor_id=vendor_id)
        if V_store.exists():
            return Response({"msg":"Already Added this details , You Can Update!"}, status=status.HTTP_400_BAD_REQUEST)

        v_store = VendorStore.objects.create(vendor_id=Vendor_management.objects.get(vendor_id=vendor_id),
                                            store_name=store_name,
                                            popular_name=popular_name,
                                            address=address, city=city,
                                            post_code=post_code,
                                            contact_person=contact_person,
                                            contact_no1=contact_no1,
                                            contact_no2=contact_no2)
        if v_store:
            return Response({"data":"Details Added Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

# update vendor store details by vendor id .... only for admin
class UpdateVendorStoreDetails(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        vendor_id = request.data.get('vendor_id', False)
        store_name = request.data.get('store_name', False)
        popular_name = request.data.get('popular_name', False)
        address = request.data.get('address', False)
        city = request.data.get('city', False)
        post_code = request.data.get('post_code', False)
        contact_person = request.data.get('contact_person', False)
        contact_no1 = request.data.get('contact_no1', False)
        contact_no2 = request.data.get('contact_no2', False)

        v_store = VendorStore.objects.filter(vendor_id__vendor_id=vendor_id).update(store_name=store_name, popular_name=popular_name,
                                                                                    address=address, city=city, post_code=post_code,
                                                                                    contact_person=contact_person, contact_no1=contact_no1,
                                                                                    contact_no2=contact_no2)
        if v_store:
            return Response({"data":"Details Updated Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


# Store Details:  -- admin panel
class AllVendorStoreDetails(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        allVendorStore = VendorStore.objects.all().values('id', 'vendorStore_id', 'store_name',
                                                          'popular_name', 'address', 'city', 'post_code',
                                                          'contact_person', 'contact_no1', 'contact_no2',
                                                          'loc_latitude', 'loc_lonitude', 'created_at',
                                                          'updated_at').annotate(
            vendor_Id=F('vendor_id__vendor_id'),
            vendor_userName=F('vendor_id__userName'),
            # vendor_password=F('vendor_id__password'),
            vendor_first_name=F('vendor_id__first_name'),
            vendor_last_name=F('vendor_id__last_name'),
            vendor_table_id=F('vendor_id__id'),
        ).order_by('-pk')

        if allVendorStore:
            return Response({"data":allVendorStore}, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"Something went wrong!"}, status=status.HTTP_400_BAD_REQUEST)


# get store details by Id   .... for admin site  .. delivery made cancel
class getStoreDetailsById(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, pk=None):
        vendor_id = request.data.get('vendor_id', False)
        # total_delivered_order = Order.objects.filter(vendor_management__vendor_id=vendor_id, delivery_status='Completed').count()
        # print("total_delivered_order")
        # print(total_delivered_order)

        # total_cancel_delivery = VendorOrderReject.objects.filter(vendor_management_Id__vendor_id=vendor_id).count()
        # print("total_cancel_delivery")
        # print(total_cancel_delivery)

        # in_process_orders = Order.objects.filter(vendor_management__vendor_id=vendor_id).exclude(delivery_status='Completed').count()
        # print("in_process_orders")
        # print(in_process_orders)

        vendor_store_details = VendorStore.objects.filter(vendor_id__vendor_id=vendor_id).values('id', 'vendorStore_id',
                                                                                                 'store_name', 'popular_name',
                                                                                                 'address', 'city', 'post_code',
                                                                                                 'contact_person', 'contact_no1',
                                                                                                 'contact_no2', 'created_at').annotate(
            vendor_userName = F('vendor_id__userName'),
            vendor_password = F('vendor_id__password'),
        )
        if vendor_store_details.exists():
            return Response({"data":vendor_store_details[0]}, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"Store Details Is not Available , Add Store !"}, status=status.HTTP_400_BAD_REQUEST)
        # print(vendor_store_details)
        # details = {"total_delivered_order":total_delivered_order, "total_cancel_delivery":total_cancel_delivery,
        #            "in_process_orders":in_process_orders, "vendor_store_details":vendor_store_details[0]}
        # if vendor_store_details:
        #     return Response(successResponseMethod(request, details), status=status.HTTP_200_OK)
        # else:
        #     return Response(errorResponseMethod(request, "Details Not Available !"), status=status.HTTP_400_BAD_REQUEST)
