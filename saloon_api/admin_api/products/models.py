from ..model_choices import *
from utility.exception_utilities import *
from utility.time_utilities import TimeUtilities
from datetime import datetime
from ..profiles.models import Profiles
from django.db import models


class Products(models.Model):
    vendor = models.ForeignKey(Profiles, on_delete=models.CASCADE, null=True)
    name = models.TextField()
    description = models.TextField()
    price = models.IntegerField()

    sales = models.IntegerField(default=0)
    timings = models.TextField()
    product_availability = models.BooleanField(default=False)
    rating = models.IntegerField(default=5)

    product_type = models.CharField(choices=PRODUCT_TYPES, max_length=1024, default=PRODUCT_TYPE_PRODUCT)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)

    @staticmethod
    def get_object_or_raise_exception(product_id):
        try:
            return Products.objects.get(pk=product_id)
        except Products.DoesNotExist:
            response = {
                'success': False,
                'detail': f'Product with id {product_id} does not exist'
            }
            raise InvalidProfileException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_object_or_none(product_id):
        try:
            return Products.objects.get(pk=product_id)
        except Products.DoesNotExist:
            return None

    def delete_product(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):

        current_time = datetime.now()

        if not self.created_at:
            self.created_at = current_time

        self.updated_at = current_time

        super(Products, self).save(*args, **kwargs)