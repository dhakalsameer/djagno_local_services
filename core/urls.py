from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('', service_list, name='service_list'),
    path('create/', service_create, name='service_create'),
    path('<int:pk>/edit/', service_update, name='service_update'),
    path('<int:pk>/delete/', service_delete, name='service_delete'),
    path('service/<int:pk>/book/', book_service, name='book_service'),
    path('service/<int:pk>/', service_detail, name='service_detail'),
    path('dashboard/provider/', provider_dashboard, name='provider_dashboard'),
    path(
    'booking/<int:booking_id>/<str:status>/',
    update_booking_status,
    name='update_booking_status'
   ),
   path('dashboard/customer/', customer_dashboard, name='customer_dashboard'),
   path('service/<int:service_id>/review/', add_review, name='add_review'),

]


urlpatterns += [
    path('service/<int:pk>/book/', book_service, name='book_service'),
]