import json
from django.db.models import Q
from rest_framework import status as status_codes
from utility.exception_utilities import CustomException
from utility.pagination_utilities import PaginationUtilities
from .serializers import OrderSerializer
from .models import Orders, Payments
from ..profiles.models import Profiles, Contact
from ..products.models import Products


class OrderService():

    order_id = None
    page = 1
    page_size = 10

    def __init__(self, order_id: str = None, page: int = 1, page_size: int = 10):
        self.set_order_id(order_id)
        self.page = page
        self.page_size = page_size

    def set_order_id(self, order_id):
        self.order_id = order_id

    def get_order_id(self):
        return self.order_id

    def _create_contact_details(self, contact_details):
        return Contact.create_contact(**contact_details)

    def _create_payment(self, payment_details, order):
        return Payments.create_payments(order = order ,**payment_details)

    def _save_order(self, profile):
        return profile.save()

    def _update_order_details(self, order, data):

        if 'time' in data:
            order.time = json.dumps(data['time'])

        order.date = data.get('date', order.date)
        order.order_status = data.get('order_status', order.order_status)

        self._save_order(order)

    def fetch_all_orders(self) -> dict:
        orders = Orders.objects.all()  # .filter(is_deleted=False)

        orders = PaginationUtilities.paginate_results(orders,
                                                      page_number=self.page,
                                                      page_size=self.page_size)

        orders_data = OrderSerializer(orders, many=True)

        response = {
            'success': True,
            'orders': orders_data.data
        }

        return response

    def fetch_order_by_id(self) -> dict:
        order = Orders.get_object_or_raise_exception(self.get_order_id())

        order_data = OrderSerializer(order)

        response = {
            'success': True,
            'order': order_data.data
        }

        return response

    def create_order(self, data) -> dict:

        if 'vendor_id' not in data:
            response = {
                'success': False,
                'error_detail': 'Send vendor id in body'
            }
            raise CustomException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

        if 'customer_id' not in data:
            response = {
                'success': False,
                'error_detail': 'Send customer id in body'
            }
            raise CustomException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

        if 'product_id' not in data:
            response = {
                'success': False,
                'error_detail': 'Send product id in body'
            }
            raise CustomException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

        try:
            data['product'] = OrderUtilities.fetch_product(data.pop('product_id'))
            data['vendor'] = OrderUtilities.fetch_profile(data.pop('vendor_id'))
            data['customer'] = OrderUtilities.fetch_profile(data.pop('customer_id'))
        except BaseException as e :
            return e.detail
        


        saved_order = None

      

        if 'payment' in data:
            payment_details = data.pop('payment')
            saved_order = self._save_order(Orders(**data))
            privacy_setting = self._create_payment(payment_details, saved_order)
            # data['payment'] = privacy_setting


        

        response = {
            'success': True,
            'order_id' : saved_order.id
        }

        return response

    def update_order(self, data) -> dict:

        order = Orders.objects.get(pk=self.get_order_id())

        if 'contact' in data:
            order.contact.update_contact(data.pop('contact'))

        if 'payment' in data:
            order.payment.update_address(data.pop('payment'))

        self._update_order_details(order, data)

        response = {
            'success': True,
        }

        return response

    def delete_order(self) -> dict:
        order = Orders.get_object_or_raise_exception(self.get_order_id())

        order.delete_order()

        response = {
            'success': True,
        }

        return response

    def search_order(self, query) -> dict:

        orders = Orders.objects.filter(Q(customer__name__icontains=query) |
                                       Q(contact__email__icontains=query) |
                                       Q(contact__phone__icontains=query))

        orders = PaginationUtilities.paginate_results(orders,
                                                      page_number=self.page,
                                                      page_size=self.page_size)

        data = OrderSerializer(orders, many=True).data

        response = {
            'success': True,
            'orders': data
        }

        return response


class OrderUtilities:

    @staticmethod
    def fetch_product(product_id):
        return Products.get_object_or_raise_exception(product_id)

    @staticmethod
    def fetch_profile(profile_id):
        return Profiles.get_object_or_raise_exception(profile_id)
