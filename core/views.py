from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import ServiceForm
from .models import Booking
from django.db.models import Q
from django.db.models import Count


# Create your views here.
@login_required
def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services/list.html', {'services': services})


@login_required
def service_create(request):
    if request.user.profile.role != 'provider':
        return redirect('service_list')

    form = ServiceForm(request.POST or None)
    if form.is_valid():
        service = form.save(commit=False)
        service.provider = request.user
        service.save()
        return redirect('service_list')
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


def home(request):
    total_services = Service.objects.filter(is_active=True).count()
    top_categories = (
        Service.objects
        .values('category__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    return render(request, 'home.html', {
        'total_services': total_services,
        'top_categories': top_categories
    })
