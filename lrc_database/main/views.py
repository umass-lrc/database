from django.shortcuts import render

from .models import Hardware, LoanForm
from .models import HardwareForm


def index(request):
    return render(request, "base.html")


def show_hardware(request):
    hardware_info = []
    for hardware in Hardware.objects.all():
        hardware_info.append({'name': hardware.name, 'availability': hardware.isAvailable})
    return render(request, 'hardware_table.html', {'hardware_info': hardware_info})


def newHardware(request):
    if request.method == 'POST':
        new_hardware = HardwareForm(request.POST)
        if new_hardware.is_valid():
            return  # redirect to new page with form validation
    else:
        new_hardware = HardwareForm()
    return render(request, 'AddHardware.html', {'new_hardware': new_hardware})


def newLoanRequest(request):
    if request.method == 'POST':
        new_loan = LoanForm(request.POST)
        if new_loan.is_valid():
            return  # redirect to new page with form validation
    else:
        new_loan = LoanForm()
    return render(request, 'AddLoan.html', {'new_loan': new_loan})
