from django.contrib.auth.models import User
from rest_framework import serializers
from dashboard.vendorModel import Vendor_management
from dashboard.productModel import Product_category, Product
from dashboard.vendorStockModel import Vendor_Stock
import re

class VendorManagementSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(label='Username', required=True)
    fullName = serializers.CharField(label='fullName', required=True)
    shopName = serializers.CharField(label='shopName', required=True)
    phone1 = serializers.CharField(label='phone1', required=True)
    phone2 = serializers.CharField(label='phone2', required=False, default='NA')
    shopAddress = serializers.CharField(label='shopAddress', required=True)
    city = serializers.CharField(label='city', required=True)
    state = serializers.CharField(label='state', required=True)
    pinCode = serializers.CharField(label='pinCode', required=True)
    email = serializers.CharField(label='email', required=False, default='example123@gmail.com')
    adhar_no = serializers.CharField(label='adhar_no', required=True)
    adhar_Img = serializers.CharField(label='adhar_Img', required=False, default='""')
    bank_name = serializers.CharField(label='bank_name', required=False, default='NA')
    bank_branch = serializers.CharField(label='bank_branch', required=False, default='NA')
    bank_address = serializers.CharField(label='bank_address', required=False, default='NA')
    ifsc_code = serializers.CharField(label='ifsc_code', required=False, default='NA')
    account_name = serializers.CharField(label='account_name', required=False, default='NA')

    # email = serializers.EmailField(label='Email Address')
    # mob_no = serializers.CharField(label='Mobile_No')

    password = serializers.CharField(label='Password')
    password2 = serializers.CharField(label='Confirm Password')

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get("password")
        password2 = value
        if password1 != password2:
            raise serializers.ValidationError("Password Must Match")

        """Validates that a password is as least 8 characters long and has at least
            2 digits and 1 Upper case letter.
            """
        msg = 'Note: password is as least 8 characters long and has at least 2 digits and 1 Upper case letter'
        min_length = 8

        if len(value) < min_length:
            raise serializers.ValidationError('Password must be at least {0} characters '
                                              'long.'.format(min_length) + msg)

        # check for 2 digits
        if sum(c.isdigit() for c in value) < 2:
            raise serializers.ValidationError('Password must container at least 2 digits.' + msg)

        # check for uppercase letter
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError('Password must container at least 1 uppercase letter.' + msg)

        return value

    # def validate_email(self, value):
    #     data = self.get_initial()
    #     email = data.get("email")
    #     regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    #     if (re.search(regex, email)):
    #         # username_qs = User.objects.filter(username=email)
    #         # if username_qs.exists():
    #         #     raise serializers.ValidationError("Email Id already exists")
    #         # else:
    #         #     pass
    #         return value
    #     raise serializers.ValidationError("invalid Email id")

    def validate_mob_no(self, value):
        data = self.get_initial()
        mob_no = data.get("mob_no")
        regex = '^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'

        if (re.search(regex, mob_no)):
            # username_qs = User.objects.filter(username=mob_no)
            # if username_qs.exists():
            #     raise serializers.ValidationError("mob_no already exists")
            # else:
            #     pass
            return value
        raise serializers.ValidationError("Phone number must be entered in the format: '9999999999',9892799999 Up to 14 digits allowed.")


    def create(self, validated_data):

        username_qs = User.objects.filter(username=validated_data['userName'])
        if username_qs.exists():
            raise serializers.ValidationError("username already exists!")

        user = Vendor_management.objects.create(
            userName=validated_data['userName'],
            fullName=validated_data['fullName'],
            shopName=validated_data['shopName'],
            phone1=validated_data['phone1'],
            phone2=validated_data['phone2'],
            shopAddress=validated_data['shopAddress'],
            city=validated_data['city'],
            state=validated_data['state'],
            pinCode=validated_data['pinCode'],
            email=validated_data['email'],
            adhar_no=validated_data['adhar_no'],
            adhar_Img=validated_data['adhar_Img'],
            bank_name=validated_data['bank_name'],
            bank_branch=validated_data['bank_branch'],
            bank_address=validated_data['bank_address'],
            ifsc_code=validated_data['ifsc_code'],
            account_name=validated_data['account_name'],
            password=validated_data['password']
        )

        return validated_data

    class Meta:
        model = Vendor_management
        fields = ('userName', 'fullName', 'shopName', 'phone1', 'phone2', 'password', 'password2', 'shopAddress',
                  'city', 'state', 'pinCode', 'email', 'adhar_no', 'adhar_Img', 'bank_name', 'bank_branch', 'bank_address',
                  'ifsc_code', 'account_name')


class GetVendorManagementSerializer(serializers.ModelSerializer):
    # payment_mode = serializers.ChoiceField(choices=Vendor_management.payment_mode_choices, required=False)

    class Meta:
        model = Vendor_management
        fields = ['id', 'vendor_id', 'vendor_register_no', 'fullName', 'shopName', 'phone1', 'phone2', 'shopAddress',
                  'city', 'state', 'pinCode', 'email', 'adhar_no', 'adhar_Img', 'bank_name', 'bank_branch', 'bank_address',
                  'ifsc_code', 'account_name', 'userName', 'login_type', 'created_at',]
        # depth = 1

class Product_CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_category
        fields = ['id', 'category_id', 'category_name', 'category_description', 'product_thumbnail', 'status'
                  ]

    def update(self, instance, validated_data):
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.category_description = validated_data.get('category_description', instance.category_description)
        instance.product_thumbnail = validated_data.get('product_thumbnail', instance.product_thumbnail)
        instance.status = validated_data.get('status', instance.status)

        instance.save()

        return instance

class Product_viewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_id', 'product_category_id', 'product_name', 'product_description', 'product_images', 'gst',
                  'product_price', 'product_status', 'discount', 'rating', 'status', 'subscription', 'created_at', 'updated_at', 'trending'
                  ]

    def update(self, instance, validated_data):
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.product_category_id = validated_data.get('product_category_id', instance.product_category_id)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_description = validated_data.get('product_description', instance.product_description)
        instance.product_images = validated_data.get('product_images', instance.product_images)
        instance.product_price = validated_data.get('product_price', instance.product_price)
        instance.product_status = validated_data.get('product_status', instance.product_status)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.status = validated_data.get('status', instance.status)
        instance.subscription = validated_data.get('subscription', instance.subscription)
        instance.gst = validated_data.get('gst', instance.gst)
        instance.trending = validated_data.get('trending', instance.trending)

        instance.save()

        return instance

# asign products to vendors
class AddProductsToVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Stock
        fields = ['id', 'vendor_id', 'product_id', 'quantity'
                  ]

    def update(self, instance, validated_data):
        instance.vendor_id = validated_data.get('vendor_id', instance.vendor_id)
        instance.product_id = validated_data.get('product_id', instance.product_id)
        # instance.product_category_id = validated_data.get('product_category_id', instance.product_category_id)
        instance.quantity = validated_data.get('quantity', instance.quantity)

        instance.save()

        return instance


