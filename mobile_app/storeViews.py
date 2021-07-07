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

# sign up vender register and store  --- used by store site
class CreateVendorManagementAndStoreDetails(CreateAPIView):
    # model = Vendor_management
    permission_classes = (AllowAny,)
    serializer_class = VendorManagementSerializer

    def post(self, request, *args, **kwargs):
        serializer = VendorManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)

        return Response({"msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# sign up vender register and store  --- used by store site --- second method
class RegisterVendorDetailsView(CreateAPIView):
    # model = Vendor_management
    permission_classes = (AllowAny,)
    serializer_class = VendorRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = VendorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)

        return Response({"msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Store Login ............ store site only
class VendorStoreLogin(ObtainAuthToken):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            password = serializer.validated_data['password']

            token, created = Token.objects.get_or_create(user=user)
            print(token.user)
            if Vendor_management.objects.filter(userName=token.user).exists():
                return Response({"token":token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"msg":"invalid User !"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# get vendor register and store details .... store site
class GetVendorsRegDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            pk = pk
            return Vendor_management.objects.get(pk=pk)
        except Vendor_management.DoesNotExist:
            raise Http404


    def get(self, request, pk=None):
        response = []
        data = Vendor_management.objects.filter(vendor_id=request.user.id)
        serializer = GetVendorManagementSerializer(data, many=True)
        print(serializer.data)
        if data:
            response = serializer.data
            # return Response(response, status=status.HTTP_200_OK)
        # return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        print(request.data)
        id = pk
        instance = self.get_object(id)
        # print(instance)
        serializer = GetVendorManagementSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data)
            return Response({"data":serializer.data})
        return Response({"msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usr = self.get_object(pk)
        print(usr.userName)
        u_sr = User.objects.get(username=str(usr.userName))
        u_sr.delete()

        usr.delete()
        return Response({"msg":"User Deleted"})
