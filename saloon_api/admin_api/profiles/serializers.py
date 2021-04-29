import json
from bson import json_util
from collections import OrderedDict  # don't remove this import
from rest_framework import serializers
from .models import Profiles, Address, Contact, PrivacySettings




class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'



class PrivacySettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivacySettings
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    #profile = ProfileSerializer(many = True, required = False)

    class Meta:
        model = Contact
        fields = ['id','phone','email']


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ('name', 'vendor_description')

class ProfileSerializer(serializers.ModelSerializer):
    profile_contacts = ContactSerializer(many=True, read_only=True)
    #address = AddressSerializer()
    
    #privacy_setting = PrivacySettingsSerializer()

    class Meta:
        model = Profiles
        fields = ['id','name','profile_contacts','profile_type','vendor_description','privacy_setting','dob','gender','image','last_app_activity','created_at','updated_at','is_deleted','is_admin_verified',]

    # def to_representation(self, profile):
    #     data = super(ProfileSerializer, self).to_representation(profile)
    #     fields = self._readable_fields

    #     for field in fields:
    #         if data[field.field_name] is None:
    #             del data[field.field_name]

    #     return data

class BasicProfileSerializer(serializers.ModelSerializer):
    profile_contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Profiles
        fields = ('id', 'name', 'profile_contacts')

