from django.urls import path
from .profile_views import (AllProfileView, DeleteProfileView,
                            UpdateProfileView, GetProfileView,
                            CreateProfileView, SearchProfileView)

urlpatterns = [
    path('', AllProfileView.as_view(), name="fetch_all_profiles"),
    path('fetch/<str:profile_id>', GetProfileView.as_view(), name="fetch_profile_by_id"),
    path('create', CreateProfileView.as_view(), name="create_profile"),
    path('update/<str:profile_id>', UpdateProfileView.as_view(), name="update_profile"),
    path('delete/<str:profile_id>', DeleteProfileView.as_view(), name="delete_profile"),
    path('search/<str:query>', SearchProfileView.as_view(), name="search_profile"),
]
