from django.urls import path
from .order_views import (AllOrdersView, GetOrderView,
                          CreateOrderView, UpdateOrderView,
                          DeleteOrderView, SearchOrderView)

urlpatterns = [
    path('', AllOrdersView.as_view(), name="fetch_all_orders"),
    path('fetch/<str:order_id>', GetOrderView.as_view(), name="fetch_order_by_id"),
    path('create', CreateOrderView.as_view(), name="create_order"),
    path('update/<str:order_id>', UpdateOrderView.as_view(), name="update_order"),
    path('delete/<str:order_id>', DeleteOrderView.as_view(), name="delete_order"),
    path('search/<str:query>', SearchOrderView.as_view(), name="search_order"),
]
