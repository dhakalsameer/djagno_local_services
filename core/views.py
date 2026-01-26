from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import ServiceForm
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
