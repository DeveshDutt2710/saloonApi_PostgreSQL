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
        list = [x[1] for x in PROFILE_TYPE]
        if value in list:
            pass
        else:
            raise ValidationError("PROFILE_TYPE must be from the list : "+(str)(list)+", in order to process correctly")
        
        
    
    def product_type_validator(value):
        list = [x[1] for x in PRODUCT_TYPES]
        if value in list:
            pass
        else:
            raise ValidationError("PRODUCT_TYPES must be from the list \n {list} \n in order to process correctly")
        
    
    def product_category_validator(value):
        list = [x[1] for x in PRODUCT_CATEGORIES]
        if value in list:
            pass
        else:
            raise ValidationError("PRODUCT_CATEGORIES must be from the list \n {list} \n in order to process correctly")
        
    def profile_gender_validator(value):
        list = [x[1] for x in PROFILE_GENDER]
        if value in list:
            pass
        else:
            raise ValidationError("PROFILE_GENDER must be from the list \n {list} \n in order to process correctly")
    
        
    def order_status_validator(value):
        list = [x[1] for x in ORDER_STATUS]
        if value in list:
            pass
        else:
            raise ValidationError("ORDER_STATUS must be from the list \n {list} \n in order to process correctly")
     
    def order_payments_validator(value):
        list = [x[1] for x in PAYMENT_STATUS]
        if value in list:
            pass
        else:
            raise ValidationError("PAYMENT_STATUS must be from the list \n {list} \n in order to process correctly")
        
   