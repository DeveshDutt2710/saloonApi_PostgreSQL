from django.urls import path, include

urlpatterns=[
    path('profiles/', include('admin_api.profiles.urls')),
]