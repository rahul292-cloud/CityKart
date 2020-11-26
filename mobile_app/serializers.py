from django.contrib.auth.models import User
from rest_framework import serializers
from dashboard.vendorModel import Vendor_management
import re

class VendorManagementSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(label='Username')
    first_name = serializers.CharField(label='first_name')
    last_name = serializers.CharField(label='last_name')

    # email = serializers.EmailField(label='Email Address')
    mob_no = serializers.CharField(label='Mobile_No')

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
    #         username_qs = User.objects.filter(username=email)
    #         if username_qs.exists():
    #             raise serializers.ValidationError("Email Id already exists")
    #         else:
    #             pass
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
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            # email=validated_data['email'],
            mob_no=validated_data['mob_no'],
            password=validated_data['password']
        )

        return validated_data

    class Meta:
        model = Vendor_management
        fields = ('userName', 'first_name', 'last_name', 'mob_no', 'password', 'password2')  # 'userName', 'email',


class GetVendorManagementSerializer(serializers.ModelSerializer):
    # payment_mode = serializers.ChoiceField(choices=Vendor_management.payment_mode_choices, required=False)

    class Meta:
        model = Vendor_management
        fields = ['id', 'vendor_id', 'userName', 'login_type', 'first_name', 'last_name', 'email',
                  'mob_no', 'image', 'created_at', 'updated_at'] # 'password',
        # depth = 1

