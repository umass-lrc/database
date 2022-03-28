from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_list_or_404, redirect, render

from .forms import AddHardwareForm, NewLoanForm
from .models import Hardware, Loan

User = get_user_model()


def restrict_to_groups(groups):
    def decorator(view):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if type(groups) is str:
                match = request.user.groups.filter(name=groups).exists()
            else:
                match = request.user.groups.filter(name__in=groups).exists()
            if match:
                return view(request, *args, **kwargs)
            raise PermissionDenied

        return _wrapped_view

    return decorator


@login_required
def index(request):
    return render(request, "base.html")


@restrict_to_groups(["Office staff", "Supervisors"])
def list_users(request, group):
    users = get_list_or_404(User, groups__name=group)
    return render(request, "list_users.html", {"users": users, "group": group})


def show_hardware(request):
    return render(request, "hardware_table.html", {"hardware": Hardware.objects.all()})


def show_loans(request):
    data = Loan.objects.all()
    return render(request, "showLoans.html", {"loanInfo": data})


def add_hardware(request):
    if request.method == "POST":
        form = AddHardwareForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        return redirect("showHardware")
    else:
        form = AddHardwareForm()
        context = {"form": form}
    return render(request, "addHardware.html", context)


def add_loans(request):
    if request.method == "POST":
        form = NewLoanForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("showLoans")
    else:
        form = NewLoanForm()
        context = {"form": form}
    return render(request, "addLoans.html", context)


def edit_loans(request, id):
    hardware = Hardware.objects.get(pk=id)
    form = AddHardwareForm(instance=hardware)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        context = {"form": form}
    return render(request, "editLoans.html", context)
