import json
from utility.pagination_utilities import PaginationUtilities
from .serializers import ProductSerializer, VendorSerializer
from rest_framework import serializers
from django.core.serializers import serialize
from ..profiles.serializers import ProfileSerializer
from .models import Products
from ..profiles.models import Profiles
from utility.exception_utilities import CustomException
from rest_framework import status as status_codes


class ProductService():

    product_id = None
    page = 1
    page_size = 10

    def __init__(self, product_id: str = None, page: int = 1, page_size: int = 10):
        self.set_product_id(product_id)
        self.page = page
        self.page_size = page_size

    def set_product_id(self, product_id):
        self.product_id = product_id

    def get_product_id(self):
        return self.product_id

    def fetch_all_products(self) -> dict:
        products = Products.objects.all()  # .filter(is_deleted=False)
        # vendorIds = Products.objects.values('vendorId')
        # vendorIds_dict = serialize(vendorIds).data
        # print(type(vendorIds_dict))

        products = PaginationUtilities.paginate_results(products,
                                                        page_number=self.page,
                                                        page_size=self.page_size)

        data = ProductSerializer(products, many=True).data

        response = {
            'success': True,
            'products': data
        }

        return response

    def fetch_product_by_id(self) -> dict:
        product = Products.get_object_or_raise_exception(self.get_product_id())

        product_data = ProductSerializer(product)

        response = {
            'success': True,
            'product': product_data.data
        }

        return response

    def create_product(self, data) -> dict:

        if 'vendor_id' not in data:
            response = {
                'success': False,
                'error_detail': 'Send vendor_id in body'
            }
            raise CustomException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

        data['vendor'] = ProductsHelper.fetch_vendor(data.pop('vendor_id'))

        saved_product_id = Products(**data).save()

        response = {
            'success': True,
            'product_id' : saved_product_id
        }

        return response

    def update_product(self, data) -> dict:

        if 'vendor_id' in data:
            data['vendor'] = ProductsHelper.fetch_vendor(data.pop('vendor_id'))

        Products.objects.filter(pk=self.get_product_id()).update(**data)

        response = {
            'success': True,
        }

        return response

    def delete_product(self) -> dict:
        product = Products.get_object_or_raise_exception(self.get_product_id())

        product.delete_product()

        response = {
            'success': True,
        }

        return response

    def search_product(self, query):

        products = Products.objects.filter(name__icontains=query)

        products = PaginationUtilities.paginate_results(products,
                                                        page_number=self.page,
                                                        page_size=self.page_size)

        product_data = ProductSerializer(products, many=True)

        response = {
            'success': True,
            'products': product_data.data
        }

        return response


class ProductsHelper:
    @staticmethod
    def fetch_vendor(vendor_id):
        return Profiles.get_object_or_raise_exception(vendor_id)