from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(ServiceImage)
admin.site.register(ServiceAvailability)
admin.site.register(Booking)
admin.site.register(Review)