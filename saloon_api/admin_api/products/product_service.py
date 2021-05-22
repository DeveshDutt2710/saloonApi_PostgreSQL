import json
from utility.pagination_utilities import PaginationUtilities
from utility.similarity_distance import SimilarityDistance
from .serializers import ProductSerializer, VendorSerializer
from rest_framework import serializers
from django.core.serializers import serialize
from ..profiles.serializers import ProfileSerializer
from .models import Products, Autocorrect
from ..profiles.models import Profiles
from utility.exception_utilities import CustomException
from rest_framework import status as status_codes
from django.db.models import Q


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

        if 'product_category' not in data:
            response = {
                'success': False,
                'error_detail': 'Send product_category in body'
            }
            raise CustomException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

        data['vendor'] = ProductsHelper.fetch_vendor(data.pop('vendor_id'))
        Autocorrect.create_autocorrect(entities=data['name'])

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

    def search_product(self, data):

        products = Products.objects.all()
        print(data)

        if 'product_category' in data:
            products = products.filter(product_category = data['product_category'])
        if 'product_type' in data:
            products = products.filter(product_type = data['product_type'])
        if 'price' in data:
            product_helper = Products.objects.none()
            for price in data['price']:
                product = products.filter(price__gte = price['min'], price__lte = price['max'])
                product_helper |= product
            products = product_helper
        if 'product_availability' in data:
            products = products.filter(product_availability = data['product_availability'])
        if 'rating' in data:
            products = products.filter(rating >= data['rating'])

        if 'query' in data:
            products = products.filter(Q(name__icontains = data['query'])
                                    |Q(vendor__name__icontains = data['query'])
                                    |Q(description__icontains = data['query']))


        products = PaginationUtilities.paginate_results(products,
                                                        page_number=self.page,
                                                        page_size=self.page_size)

        product_data = ProductSerializer(products, many=True)

        response = {
            'success': True,
            'products': product_data.data
        }

        return response
    
    def autocorrect_query(self, data):
        entities = list(Autocorrect.objects.values_list('entities', flat=True))

        list_display = []
        for key in entities:
            if(SimilarityDistance.get_similarity_distance(data['query'], str(key),len(data['query']), len(str(key))) < 5):
                if((str(key))[0] == data['query'][0]):
                    list_display.append(str(key))

        response = {
            'success': True,
            'suggestions' : list_display
        }

        return response


class ProductsHelper:
    @staticmethod
    def fetch_vendor(vendor_id):
        return Profiles.get_object_or_raise_exception(vendor_id)