from rest_framework.exceptions import APIException
from rest_framework import status as status_codes


class BaseException(APIException):
    status_code = status_codes.HTTP_400_BAD_REQUEST
    default_code = 'bad  request'
    default_detail = 'Service temporarily unavailable, try again later.'

    def __init__(self, detail=None, status_code=None):
        if detail is not None:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class CustomException(BaseException):
    detail = {"success": False,
              "error_message": "Something went wrong"
              }


class InvalidHeaderException(BaseException):
    detail = {"success": False,
              "error_message": "send member id in headers"
              }


class InvalidProfileException(BaseException):
    detail = {"success": False,
              "error_message": "Profile does not exist"
              }


class InvalidAccountException(BaseException):
    detail = {"success": False,
              "error_message": "Account does not exist"
              }


class InvalidOrderException(BaseException):
    detail = {"success": False,
              "error_message": "Order does not exist"
              }


class InvalidProductException(BaseException):
    detail = {"success": False,
              "error_message": "Product does not exist"
              }


class InvalidEnquiryException(BaseException):
    detail = {"success": False,
              "error_message": "Enquiry does not exist"
              }
