from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import AddHardwareForm, NewLoanForm
from .models import Hardware, Loan


def index(request):
    return render(request, "base.html")


def show_hardware(request):
    addForm = AddHardwareForm()
    hardware_info = []
    for hardware in Hardware.objects.all():
        hardware_info.append({'name': hardware.name, 'availability': hardware.isAvailable})
    context = {'hardware_info': hardware_info, 'addForm': addForm}
    return render(request, 'hardware_table.html', context)


def show_loans(request):
    newLoanForm = NewLoanForm()
    loan_info = []
    for loans in Loan.objects.all():
        loan_info.append({'target': loans.target, 'hardware_user': loans.hardware_user,
                          'start_time': loans.start_time, 'return_time': loans.return_time})
    context = {'loan_info': loan_info, 'newLoanForm': newLoanForm}
    return render(request, 'showLoans.html', context)


@require_POST
def add_hardware(request):
    form = AddHardwareForm(request.POST)
    if form.is_valid():
        new_hardware = Hardware(name=request.POST['name'], is_available=request.POST['is_available'])
        new_hardware.save()
    return  # redirect('show_hardware')


@require_POST
def add_loan(request):
    form = NewLoanForm(request.POST)
    if form.is_valid():
        new_loan = Loan(target=request.POST['target'], hardware_user=request.POST['hardware_user'],
                        start_time=request.POST['start_time'], return_time=request.POST['return_time'])
        new_loan.save()
    return  # redirect('show_loans')


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
