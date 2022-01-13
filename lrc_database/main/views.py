from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Hardware


def show_hardware(request):
    hardware_info = []
    for hardware in Hardware.objects.all():
        hardware_info.append({'name': hardware.name, 'availability': hardware.isAvailable})
    return render_to_response('hardware_table.html', {'hardware_info': hardware_info},
                              context_instance=RequestContext(request))
