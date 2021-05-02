import json
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from admin_api.model_choices import *

class Utilities:

    @staticmethod
    def convert_string_to_json(json_string):
        try:
            return json.loads(json_string)
        except:
            return eval(json_string)

class ModelChoicesUtilities:

    def profile_type_validator(value):
        if value not in [x[1] for x in PROFILE_TYPE]:
            raise ValidationError(
                _('%(value)s is not in the choices list'),
                params={'value': value},
            )
    
    def product_type_validator(value):
        if value not in [x[1] for x in PRODUCT_TYPES]:
            raise ValidationError(
                _('%(value)s is not in the choices list'),
                params={'value': value},
            )
    
    def product_category_validator(value):
        if value not in [x[1] for x in PRODUCT_CATEGORIES]:
            raise ValidationError(
                _('%(value)s is not in the choices list'),
                params={'value': value},
            )
        
    def profile_gender_validator(value):
        if value not in [x[1] for x in PROFILE_GENDER]:
            raise ValidationError(
                _('%(value)s is not in the choices list'),
                params={'value': value},
            )
        
    def order_status_validator(value):
        if value not in [x[1] for x in ORDER_STATUS]:
            raise ValidationError(
                _('%(value)s is not in the choices list'),
                params={'value': value},
            )
    
    def order_payments_validator(value):
        if value not in [x[1] for x in PAYMENT_STATUS]:
            raise ValidationError(
                _('%(value)s is not in the choices list'),
                params={'value': value},
            )
