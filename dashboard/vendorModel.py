from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
import datetime
import random, string


def randomword(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

def randomNo():
    return random.randint(1000,9999)

class Vendor_management(models.Model):
    referal_code = models.IntegerField(default=randomNo)
    referal_code_by_other = models.IntegerField(default=0, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$',
                                 message="Phone number must be entered in the format: '999999999',0989279999 Up to 14 digits allowed.")
    email_regex = RegexValidator(regex=r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
                                 message="Email Id must be entered in the format: example326@gmail.com' Up to 50 character allowed.")

    vendor_id = models.IntegerField(null=True, blank=True)
    vendor_register_no = models.IntegerField(default=randomNo)
    fullName = models.CharField(max_length=500, null=True, blank=False)
    homeAddress = models.CharField(max_length=1000, null=True, blank=True)
    phone_self = models.CharField(validators=[phone_regex], max_length=15, null=True, blank=False)
    shopName = models.CharField(max_length=500, null=True, blank=False)

    shop_type_choices = (
        ('General Store', 'General Store'),
        ('Footwear', 'Footwear'),
        ('Electronics', 'Electronics'),
        ('Others', 'Others'),
    )

    shop_type = models.CharField(null=True, blank=True, max_length=200, choices=shop_type_choices)
    phone_shop = models.CharField(validators=[phone_regex], max_length=15, null=True, blank=True)


    # phone1 = models.CharField(max_length=500, null=True, blank=False)
    # phone2 = models.CharField(max_length=500, null=True, blank=True)
    shopAddress = models.CharField(max_length=1000, null=True, blank=False)
    city = models.CharField(max_length=500, null=True, blank=False)
    state = models.CharField(max_length=500, null=True, blank=False)

    pinCode = models.CharField(max_length=500, null=True, blank=False, unique=True)
    email = models.CharField(validators=[email_regex], max_length=500, null=True, blank=True)

    adhar_no  = models.CharField(max_length=500, null=True, blank=False)
    adhar_Img = models.FileField(blank=True, null=True, upload_to='adharImages/')

    pAN_no = models.CharField(max_length=500, null=True, blank=True)
    pAN_Img = models.FileField(blank=True, null=True, upload_to='PAN_Images/')

    business_adhar_no = models.CharField(max_length=500, null=True, blank=True)
    business_adhar_Img = models.FileField(blank=True, null=True, upload_to='BusinessAdharImages/')

    business_pAN_no = models.CharField(max_length=500, null=True, blank=True)
    business_pAN_Img = models.FileField(blank=True, null=True, upload_to='BusinessPAN_Images/')

    gSTIN_no = models.CharField(max_length=500, null=True, blank=True)

    bank_name = models.CharField(max_length=500, null=True, blank=True)
    bank_branch = models.CharField(max_length=500, null=True, blank=True)
    bank_address = models.CharField(max_length=1000, null=True, blank=True)
    ifsc_code = models.CharField(max_length=500, null=True, blank=True)
    account_name = models.CharField(max_length=500, null=True, blank=True)
    account_no = models.CharField(max_length=500, null=True, blank=True)

    subscription_from = models.DateField(null=True, blank=True)
    subscription_to = models.DateField(null=True, blank=True)

    vendor_status = models.BooleanField(default=True)

    userName = models.CharField(max_length=500, null=True, blank=False)
    login_type = models.CharField(max_length=500, null=True, blank=True, default='Vendor')

    password = models.CharField(max_length=20, null=True, blank=False)
    # mob_no = models.CharField(validators=[phone_regex], max_length=15, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    loc_latitude = models.FloatField(null=True, blank=True)
    loc_lonitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.userName


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk is None:
            self.vendor_register_no = randomNo()
            self.referal_code = randomNo()
            self.created_at = datetime.datetime.now()
            self.subscription_from = datetime.datetime.now()
            self.subscription_to = datetime.datetime.now() + datetime.timedelta(days=365)
            usr_name = self.userName
            print(usr_name)
            user_obj = User.objects.create_user(
                username=usr_name, password=self.password, is_staff=False,
                first_name=self.fullName, last_name=self.fullName
            )  #  email=self.email,
            user_data = list(User.objects.filter(username=user_obj).values('pk'))
            user_data[0].get('pk')
            print(user_data[0].get('pk'))
            self.vendor_id = user_data[0].get('pk')
            self.user_id = user_data[0].get('pk')
            res = super(Vendor_management, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            res = super(Vendor_management, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return res

# class Vendor_management(models.Model):
#     phone_regex = RegexValidator(regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$',
#                                  message="Phone number must be entered in the format: '999999999',0989279999 Up to 14 digits allowed.")
#     email_regex = RegexValidator(regex=r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
#                                  message="Email Id must be entered in the format: example326@gmail.com' Up to 50 character allowed.")
#
#     vendor_id = models.IntegerField(null=True, blank=True)
#
#     userName = models.CharField(max_length=500, null=True, blank=True)
#     login_type = models.CharField(max_length=500, null=True, blank=True, default='Vendor')
#     first_name = models.CharField(max_length=100, null=True, blank=True)
#     last_name = models.CharField(max_length=100, null=True, blank=True)
#     email = models.CharField(validators=[email_regex], max_length=500, null=True, blank=True)
#     password = models.CharField(max_length=20, null=True, blank=True)
#     mob_no = models.CharField(validators=[phone_regex], max_length=15, null=True)
#     # OTP = models.IntegerField(null=True, blank=True)
#     address1 = models.CharField(max_length=500, null=True, blank=True)
#     address2 = models.CharField(max_length=500, null=True, blank=True)
#     pincode = models.IntegerField(null=True, blank=True)
#     notes = models.TextField(null=True, blank=True)
#     id_proof = models.CharField(max_length=500, null=True, blank=True)
#     image = models.CharField(max_length=500, null=True, blank=True)
#     payment_status = models.BooleanField(default=False)
#
#     payment_mode_choices = (
#         ('wallet', 'wallet'),
#         ('cod', 'cod'),
#         ('debit_card', 'debit_card'),
#         ('credit_card', 'credit_card'),
#     )
#
#     payment_mode = models.CharField(null=True, blank=True, max_length=20, choices=payment_mode_choices)
#
#     status = models.BooleanField(default=False)
#     created_at = models.DateTimeField(null=True, blank=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     loc_latitude = models.FloatField(null=True, blank=True)
#     loc_lonitude = models.FloatField(null=True, blank=True)
#
#     def __str__(self):
#         return self.userName
#
#
#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#
#         if self.pk is None:
#             self.created_at = datetime.datetime.now()
#             usr_name = self.userName
#             print(usr_name)
#             user_obj = User.objects.create_user(
#                 username=usr_name, password=self.password, is_staff=False,
#                 first_name=self.first_name, last_name=self.last_name
#             )  #  email=self.email,
#             user_data = list(User.objects.filter(username=user_obj).values('pk'))
#             user_data[0].get('pk')
#             print(user_data[0].get('pk'))
#             self.vendor_id = user_data[0].get('pk')
#             self.user_id = user_data[0].get('pk')
#             res = super(Vendor_management, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
#         else:
#             self.updated_at = datetime.datetime.now()
#             res = super(Vendor_management, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
#         return res