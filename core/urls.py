from django.urls import path
from .views import *

urlpatterns = [
    path('', service_list, name='service_list'),
    path('create/', service_create, name='service_create'),
    path('<int:pk>/edit/', service_update, name='service_update'),
    path('<int:pk>/delete/', service_delete, name='service_delete'),
    path('service/<int:pk>/book/', book_service, name='book_service'),

]
