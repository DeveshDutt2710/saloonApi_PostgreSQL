from django.urls import path
from .product_views import (AllProductsView, GetProductView,
                            CreateProductView, UpdateProductView,
                            DeleteProductView, SearchProductView,AutocorrectView)

urlpatterns = [
    path('', AllProductsView.as_view(), name="fetch_all_products"),
    path('fetch/<str:product_id>', GetProductView.as_view(), name="fetch_product_by_id"),
    path('create', CreateProductView.as_view(), name="create_product"),
    path('update/<str:product_id>', UpdateProductView.as_view(), name="update_product"),
    path('delete/<str:product_id>', DeleteProductView.as_view(), name="delete_product"),
    path('search/', SearchProductView.as_view(), name="search_product"),
    path('autocorrect/',AutocorrectView.as_view(), name="auto_correct"),
]
