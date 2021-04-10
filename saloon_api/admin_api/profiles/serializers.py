import json
from bson import json_util
from collections import OrderedDict  # don't remove this import
from rest_framework import serializers
from .models import Profiles, Address, Contact, PrivacySettings


class BasicProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='contact.email')
    phone = serializers.ReadOnlyField(source='contact.phone')

    class Meta:
        model = Profiles
        fields = ('id', 'name', 'email', 'phone')


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'


class PrivacySettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivacySettings
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    contact = ContactSerializer()
    privacy_setting = PrivacySettingsSerializer()

    class Meta:
        model = Profiles
        fields = '__all__'

    def to_representation(self, profile):
        data = super(ProfileSerializer, self).to_representation(profile)
        fields = self._readable_fields

        for field in fields:
            if data[field.field_name] is None:
                del data[field.field_name]

        return data
