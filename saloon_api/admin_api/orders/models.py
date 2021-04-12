from ..model_choices import *
from utility.exception_utilities import *
from utility.time_utilities import TimeUtilities
from datetime import datetime
from django.db import models
from ..profiles.models import Profiles, Contact
from ..products.models import Products


class Payments(models.Model):
    status = models.CharField(choices=PAYMENT_STATUS, max_length=1024, default=PAYMENT_STATUS_PENDING)
    amount = models.IntegerField()
    details = models.TextField()

    @staticmethod
    def create_payments(data):
        address = Payments(**data)
        address.save()

        return address

    def update_address(self, data):
        self.status = data.get('status', self.status)
        self.amount = data.get('amount', self.amount)
        self.details = data.get('details', self.details)
        self.save()


class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='vendor_id', null=True)
    customer = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='customer_id', null=True)

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)

    payment = models.ForeignKey(Payments, on_delete=models.CASCADE, null=True)

    time = models.TextField()

    date = models.DateTimeField(auto_now_add=True)

    order_status = models.CharField(choices=ORDER_STATUS, max_length=1024, default=ORDER_STATUS_UPCOMING)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)

    @staticmethod
    def get_object_or_raise_exception(order_id):
        try:
            return Orders.objects.get(pk=order_id)
        except Orders.DoesNotExist:
            response = {
                'success': False,
                'detail': f'Order with id {order_id} does not exist'
            }
            raise InvalidProfileException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_object_or_none(order_id):
        try:
            return Orders.objects.get(pk=order_id)
        except Orders.DoesNotExist:
            return None

    def delete_order(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):

        current_time = datetime.now()

        if not self.created_at:
            self.created_at = current_time

        self.updated_at = current_time

        super(Orders, self).save(*args, **kwargs)
