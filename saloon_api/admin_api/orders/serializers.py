import json
from collections import OrderedDict  # don't remove this import
from rest_framework import serializers
from .models import Orders, Payments
from ..profiles.serializers import BasicProfileSerializer, ContactSerializer, ProfileSerializer
from ..products.serializers import BasicProductSerializer, ProductSerializer
from utility.utilities import Utilities


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orders_payments_rn = PaymentSerializer(many = True, read_only = True)
    # order_product_rn = ProductSerializer(many = True, read_only = True)
    # order_vendor_rn = ProfileSerializer(many = True, read_only = True)
    # order_customer_rn = ProfileSerializer(many = True, read_only = True)

    class Meta:
        model = Orders
        fields = ['product','vendor','customer','orders_payments_rn']
        depth = 2

    # def to_representation(self, order):
    #     data = super(OrderSerializer, self).to_representation(order)
    #     fields = self._readable_fields

    #     for field in fields:

    #         if field.field_name == 'time' and data[field.field_name] is not None:
    #             data[field.field_name] = Utilities.convert_string_to_json(data[field.field_name])

    #         elif data[field.field_name] is None:
    #             del data[field.field_name]

    #     return data
