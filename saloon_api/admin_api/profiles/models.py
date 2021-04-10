from ..model_choices import *
from utility.exception_utilities import *
from utility.time_utilities import TimeUtilities
from datetime import datetime
from django.db import models


class PrivacySettings(models.Model):
    profile = models.ForeignKey('Profiles', on_delete=models.CASCADE, null=True)
    contact_setting = models.BooleanField(default=True)
    address_setting = models.BooleanField(default=True)

    @staticmethod
    def create_privacy_setting(data):
        privacy_setting = PrivacySettings(**data)
        privacy_setting.save()

        return privacy_setting

    def update_privacy_setting(self, data):
        self.contact_setting = data.get('contact_setting', self.contact_setting)
        self.address_setting = data.get('address_setting', self.address_setting)
        self.save()



class Address(models.Model):
    house_no = models.CharField(max_length=100, blank=True)
    locality = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    landmark = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=100, blank=True)

    @staticmethod
    def create_address(data):
        address = Address(**data)
        address.save()

        return address

    def update_address(self, data):
        self.house_no = data.get('house_no', self.house_no)
        self.locality = data.get('locality', self.locality)
        self.street = data.get('street', self.street)
        self.landmark = data.get('landmark', self.landmark)
        self.city = data.get('city', self.city)
        self.state = data.get('state', self.state)
        self.country = data.get('country', self.country)
        self.pincode = data.get('pincode', self.pincode)
        self.save()



class Contact(models.Model):
    phone = models.BigIntegerField()
    email = models.EmailField()

    @staticmethod
    def create_contact(email, phone):
        contact = Contact(email=email, phone=phone)
        contact.save()

        return contact

    def update_contact(self, data):
        self.phone = data.get('phone', self.phone)
        self.email = data.get('email', self.email)
        self.save()


class Profiles(models.Model):
    name = models.CharField(max_length=255, null=False)
    #account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
    profile_type = models.CharField(choices=PROFILE_TYPE, max_length=1024, default=PROFILE_TYPE_CUSTOMER)

    vendor_description = models.TextField(null=True)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='profile_contact_details')

    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='profile_address_details', null=True)

    privacy_setting = models.OneToOneField(PrivacySettings, on_delete=models.CASCADE, null=True)

    dob = models.DateTimeField()

    gender = models.CharField(max_length=10)
    image = models.TextField()

    last_app_activity = models.DateTimeField(null=True)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)
    is_admin_verified = models.BooleanField(default=False)

    my_coupons = models.TextField()

    def update_privacy_setting(self, data):
        self.name = data.get('name', self.name)
        self.account = data.get('account', self.account)
        self.profile_type = data.get('profile_type', self.profile_type)
        self.vendor_description = data.get('vendor_description', self.vendor_description)
        self.dob = data.get('dob', self.dob)
        self.gender = data.get('gender', self.gender)
        self.image = data.get('image', self.image)
        self.last_app_activity = data.get('last_app_activity', self.last_app_activity)
        self.is_deleted = data.get('is_deleted', self.is_deleted)
        self.is_admin_verified = data.get('is_admin_verified', self.is_admin_verified)
        self.save()

    @staticmethod
    def get_object_or_raise_exception(profile_id):
        try:
            return Profiles.objects.get(pk=profile_id)
        except Profiles.DoesNotExist:
            response = {
                'success': False,
                'detail': f'Profile with id {profile_id} does not exist'
            }
            raise InvalidProfileException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_object_or_none(profile_id):
        try:
            return Profiles.objects.get(pk=profile_id)
        except Profiles.DoesNotExist:
            return None

    def delete_profile(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):

        current_time = datetime.now()

        if not self.created_at:
            self.created_at = current_time

        self.updated_at = current_time

        super(Profiles, self).save(*args, **kwargs)

