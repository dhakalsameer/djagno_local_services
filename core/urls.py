from django.urls import path
from .views import *

urlpatterns = [

    # 🏠 Home
    path('', home, name='home'),

    # 🛠 Services
    path('services/', service_list, name='service_list'),
    path('services/create/', service_create, name='service_create'),
    path('services/<int:pk>/', service_detail, name='service_detail'),
    path('services/<int:pk>/edit/', service_update, name='service_update'),
    path('services/<int:pk>/delete/', service_delete, name='service_delete'),

    # 📅 Booking
    path('services/<int:pk>/book/', book_service, name='book_service'),

    # 📊 Dashboards
    path('dashboard/provider/', provider_dashboard, name='provider_dashboard'),
    path('dashboard/customer/', customer_dashboard, name='customer_dashboard'),

    # ✅ Booking actions
    path(
        'booking/<int:booking_id>/<str:status>/',
        update_booking_status,
        name='update_booking_status'
    ),

    # ⭐ Reviews
    path(
        'services/<int:service_id>/review/',
        add_review,
        name='add_review'
    ),
]
