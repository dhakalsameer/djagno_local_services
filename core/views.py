from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review, Service, ServiceCategory
from .forms import ServiceForm
from .models import Booking
from django.db.models import Q
from django.db.models import Count
from django.db.models import Avg, Count
from .models import Service, Booking
from datetime import date
from .forms import ReviewForm
from .utils import auto_complete_bookings
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
@login_required
def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/list.html', {'services': services})


@login_required
def service_create(request):
    # Only service providers can create services
    if request.user.profile.role != 'provider':
        return redirect('service_list')

    form = ServiceForm(request.POST or None, request.FILES or None, user=request.user)

    if form.is_valid():
        service = form.save(commit=False)
        service.provider = request.user  # Assign logged-in user automatically

        # Handle new category if entered
        new_cat_name = form.cleaned_data.get('new_category')
        if new_cat_name:
            # This assumes ServiceCategory now has 'provider' ForeignKey
            category, created = ServiceCategory.objects.get_or_create(
                name=new_cat_name.strip(),
                provider=request.user
            )
            service.category = category
        else:
            # Assign selected category from form (if any)
            service.category = form.cleaned_data.get('category')

        service.save()
        form.save_m2m()  # If form has ManyToMany fields
        return redirect('provider_dashboard')

    return render(request, 'services/form.html', {'form': form})




@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        return redirect('provider_dashboard')
    return render(request, 'services/form.html', {'form': form})


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    service.delete()
    return redirect('service_list')


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings

@login_required
def book_service(request, pk):
    service = get_object_or_404(Service, pk=pk)

    # 🚫 Providers cannot book services
    if hasattr(request.user, 'profile') and request.user.profile.role == 'provider':
        return HttpResponseForbidden("Providers cannot book services.")

    if request.method == 'POST':
        booking_date = request.POST.get('date')
        start = request.POST.get('start')
        end = request.POST.get('end')

        exists = Booking.objects.filter(
            service=service,
            booking_date=booking_date,
            start_time=start,
            status__in=['pending', 'accepted']
        ).exists()

        if not exists:
            booking = Booking.objects.create(
                customer=request.user,
                service=service,
                booking_date=booking_date,
                start_time=start,
                end_time=end
            )

            # 📧 Email to provider
            send_mail(
                subject='New Service Booking',
                message=f"""
You have a new booking request.

Service: {service.title}
Date: {booking.booking_date}
Time: {booking.start_time} - {booking.end_time}
Customer: {request.user.username}
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[service.provider.email],
                fail_silently=False,
            )

            # 📧 Email to customer
            send_mail(
                subject='Booking Submitted',
                message=f"""
Your booking request has been sent.

Service: {service.title}
Date: {booking.booking_date}
Time: {booking.start_time} - {booking.end_time}
Status: Pending approval
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            return redirect('customer_dashboard')

    return render(request, 'booking/book.html', {'service': service})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)

    can_review = False

    if request.user.is_authenticated and request.user.profile.role == 'customer':
        can_review = Booking.objects.filter(
            service=service,
            customer=request.user,
            status='completed'
        ).exists()

    return render(request, 'services/detail.html', {
        'service': service,
        'can_review': can_review,
    })




@login_required
def home(request):
    total_services = Service.objects.filter(is_active=True).count()

    # Top 5 rated services
    top_services = (
        Service.objects
        .annotate(avg_rating=Avg('reviews__rating'))
        .order_by('-avg_rating')[:5]
    )

    # Top 5 most booked services
    most_booked = (
        Service.objects
        .annotate(total_bookings=Count('bookings'))
        .order_by('-total_bookings')[:5]
    )

    # Determine user role
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'customer'

    # For customers, get the IDs of services they have already booked
    booked_service_ids = []
    if user_role != 'provider':
        booked_service_ids = Booking.objects.filter(customer=request.user) \
                                            .values_list('service_id', flat=True)

    return render(request, 'home.html', {
        'total_services': total_services,
        'top_services': top_services,
        'most_booked': most_booked,
        'user_role': user_role,
        'booked_service_ids': booked_service_ids,  # pass to template
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


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)

    # 🚫 Only provider can update
    if request.user != booking.service.provider:
        return HttpResponseForbidden("You are not allowed to do this.")

    # 🚫 Only allow these actions
    if status not in ['accepted', 'cancelled']:
        return redirect('provider_dashboard')

    # 🚫 Only pending bookings can be accepted or cancelled
    if booking.status != 'pending':
        return redirect('provider_dashboard')

    booking.status = status
    booking.save()

    # 📧 EMAIL TO CUSTOMER
    subject = f"Booking {status.title()} – {booking.service.title}"

    html_content = render_to_string(
        'emails/booking_status.html',
        {
            'booking': booking,
            'status': status,
        }
    )

    text_content = f"""
Your booking has been {status}.

Service: {booking.service.title}
Date: {booking.booking_date}
Status: {status.title()}
"""

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [booking.customer.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

    return redirect('provider_dashboard')


@login_required
def customer_dashboard(request):
    auto_complete_bookings()
    ...
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    services = Service.objects.filter(is_active=True)
    today = date.today()
    booked_service_ids = bookings.values_list('service_id', flat=True)

    return render(request, 'dashboard/customer.html', {
        'bookings': bookings,
        'services': services,
        'today': today,
        'user_role': request.user.profile.role,
        'booked_service_ids': booked_service_ids,
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
    
    # ❌ Prevent duplicate review
    if Review.objects.filter(service=service, customer=request.user).exists():
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


@login_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.service.provider != request.user:
        return HttpResponseForbidden()

    if booking.status == 'accepted':
        booking.status = 'completed'
        booking.save()

    return redirect('provider_dashboard')
