import json
from collections import OrderedDict  # don't remove this import
from rest_framework import serializers
from .models import Products
from ..profiles.serializers import BasicProfileSerializer, VendorSerializer, ProfileSerializer
from utility.utilities import Utilities





class BasicProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'name', 'description', 'price')

class ProductSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = Products
        fields = '__all__'

    # def to_representation(self, profile):
    #     data = super(ProductSerializer, self).to_representation(profile)
    #     fields = self._readable_fields

    #     for field in fields:

    #         if field.field_name == "timings" and data[field.field_name] is not None:
    #             data[field.field_name] = Utilities.convert_string_to_json(data[field.field_name])

    #         if data[field.field_name] is None:
    #             del data[field.field_name]

    #     return data

