from django.contrib import admin
from .profiles.models import Profiles, Contact, PrivacySettings, Address
from .products.models import Products
from .orders.models import Orders, Payments


# Register your models here.
admin.site.register(Profiles)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Contact)
admin.site.register(PrivacySettings)
admin.site.register(Address)
admin.site.register(Payments)
