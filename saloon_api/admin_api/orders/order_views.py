from rest_framework.views import APIView
from rest_framework import status as status_codes
from django.http import JsonResponse
from .order_service import OrderService
from ..mixins import TransactionMixin


class AllOrdersView(APIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        page_no = query_params.get('page', 1)
        page_size = query_params.get("page_size", 10)

        order_manager = OrderService(page=page_no, page_size=page_size)
        response = order_manager.fetch_all_orders()

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class GetOrderView(APIView):

    def get(self, request, order_id, *args, **kwargs):

        order_manager = OrderService(order_id)
        response = order_manager.fetch_order_by_id()

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class CreateOrderView(TransactionMixin, APIView):

    def post(self, request, *args, **kwargs):

        order_manager = OrderService()
        response = order_manager.create_order(request.data)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class UpdateOrderView(TransactionMixin, APIView):

    def post(self, request, order_id, *args, **kwargs):

        order_manager = OrderService(order_id)
        response = order_manager.update_order(request.data)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class DeleteOrderView(TransactionMixin, APIView):

    def post(self, request, order_id, *args, **kwargs):

        order_manager = OrderService(order_id)
        response = order_manager.delete_order()

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class SearchOrderView(APIView):

    def post(self, request, query, *args, **kwargs):
        query_params = request.query_params

        page_no = query_params.get('page', 1)
        page_size = query_params.get("page_size", 10)

        order_manager = OrderService(page=page_no, page_size=page_size)
        response = order_manager.search_order(query)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)
