from django.shortcuts import render

from .models import Hardware


def show_hardware(request):
    hardware_info = []
    for hardware in Hardware.objects.all():
        hardware_info.append({'name': hardware.name, 'availability': hardware.isAvailable})
    return render(request, 'hardware_table.html', {'hardware_info': hardware_info})
