from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, ServiceCategory
from .forms import ServiceForm
from .models import Booking
from django.db.models import Q
from django.db.models import Count
from django.db.models import Avg, Count
from .models import Service, Booking
from datetime import date
from .forms import ReviewForm
from .utils import auto_complete_bookings


# Create your views here.
@login_required
def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/list.html', {'services': services})


@login_required
def service_create(request):
    if request.user.profile.role != 'provider':
        return redirect('service_list')

    form = ServiceForm(request.POST or None, request.FILES or None, user=request.user)
    if form.is_valid():
        service = form.save(commit=False)
        
        # Check if provider entered a new category
        new_cat_name = form.cleaned_data.get('new_category')
        if new_cat_name:
            category, created = ServiceCategory.objects.get_or_create(
                name=new_cat_name,
                provider=request.user
            )
            service.category = category

        service.provider = request.user
        service.save()
        return redirect('provider_dashboard')

    return render(request, 'services/form.html', {'form': form})



@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        return redirect('service_list')
    return render(request, 'services/form.html', {'form': form})


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    service.delete()
    return redirect('service_list')


@login_required
def book_service(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        date = request.POST['date']
        start = request.POST['start']
        end = request.POST['end']

        exists = Booking.objects.filter(
            service=service,
            booking_date=date,
            start_time=start,
            status__in=['pending', 'accepted']
        ).exists()     

        if not exists:
            Booking.objects.create(
                customer=request.user,
                service=service,
                booking_date=date,
                start_time=start,
                end_time=end
            )
            return redirect('service_list')

    return render(request, 'booking/book.html', {'service': service})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)

    return render(request, 'services/detail.html', {
        'service': service
    })



@login_required
def home(request):
    total_services = Service.objects.filter(is_active=True).count()

    top_services = (
        Service.objects
        .annotate(avg_rating=Avg('reviews__rating'))
        .order_by('-avg_rating')[:5]
    )

    most_booked = (
        Service.objects
        .annotate(total_bookings=Count('bookings'))
        .order_by('-total_bookings')[:5]
    )

    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'customer'

    return render(request, 'home.html', {
        'total_services': total_services,
        'top_services': top_services,
        'most_booked': most_booked,
        'user_role': user_role
    })



@login_required
def book_service(request, pk):
    service = get_object_or_404(Service, pk=pk)

    error = None

    if request.method == 'POST':
        booking_date = request.POST['date']
        start_time = request.POST['start']
        end_time = request.POST['end']

        exists = Booking.objects.filter(
            service=service,
            booking_date=booking_date,
            start_time=start_time,
            status__in=['pending', 'accepted']
        ).exists()

        if exists:
            error = "This time slot is already booked."
        else:
            Booking.objects.create(
                customer=request.user,
                service=service,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time
            )
            return redirect('service_detail', pk=service.id)

    return render(request, 'booking/book.html', {
        'service': service,
        'today': date.today(),
        'error': error
    })




@login_required
def provider_dashboard(request):
    auto_complete_bookings()
    ...
    if request.user.profile.role != 'provider':
        return redirect('home')

    services = Service.objects.filter(provider=request.user)
    bookings = Booking.objects.filter(
        service__provider=request.user
    ).order_by('-created_at')

    return render(request, 'dashboard/provider.html', {
        'services': services,
        'bookings': bookings
    })


@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        service__provider=request.user
    )

    if status in ['accepted', 'cancelled']:
        booking.status = status
        booking.save()

    return redirect('provider_dashboard')

@login_required
def customer_dashboard(request):
    auto_complete_bookings()
    ...
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    services = Service.objects.filter(is_active=True)
    today = date.today()

    return render(request, 'dashboard/customer.html', {
        'bookings': bookings,
        'services': services,
        'today': today,
        'user_role': request.user.profile.role,
    })


@login_required
def add_review(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    has_completed = Booking.objects.filter(
        service=service,
        customer=request.user,
        status='completed'
    ).exists()

    if not has_completed:
        return redirect('service_detail', pk=service.id)

    form = ReviewForm(request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.service = service
        review.customer = request.user
        review.save()
        return redirect('service_detail', pk=service.id)

    return render(request, 'reviews/add.html', {
        'form': form,
        'service': service
    })
