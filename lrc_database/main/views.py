from django.shortcuts import render

from .forms import AddHardwareForm, NewLoanForm
from .models import Hardware, Loan


def index(request):
    return render(request, "base.html")


def show_hardware(request):
    hardware_info = []
    for hardware in Hardware.objects.all():
        hardware_info.append({'name': hardware.name, 'availability': hardware.is_available})
    context = {'hardware_info': hardware_info}
    return render(request, 'hardware_table.html', context)


def show_loans(request):
    loan_info = []
    for loans in Loan.objects.all():
        loan_info.append({'target': loans.target, 'hardware_user': loans.hardware_user,
                          'start_time': loans.start_time, 'return_time': loans.return_time})
    context = {'loan_info': loan_info}
    return render(request, 'showLoans.html', context)


def add_hardware(request):
    form = AddHardwareForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {
        'form': form
    }
    return render(request, 'addHardware.html', context)


def add_loans(request):
    form = NewLoanForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        context = {
            'form': form
        }
    return render(request, 'addLoans.html', context)


def edit_hardware(request, id):
    hardware = Hardware.objects.get(pk=id)
    form = AddHardwareForm(instance=hardware)
    form.save()
    return  # redirect ('show_hardware')


def edit_loan(request, id):
    loan = Loan.objects.get(pk=id)
    form = NewLoanForm(instance=loan)
    form.save()
    return  # redirect ('show_hardware')
