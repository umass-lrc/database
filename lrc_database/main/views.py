import json
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse

from .forms import (
    AddHardwareForm,
    CourseForm,
    CreateUserForm,
    CreateUsersInBulkForm,
    EditProfileForm,
    NewChangeRequestForm,
    NewLoanForm,
)
from .models import Course, Hardware, Loan, LRCDatabaseUser, Shift, ShiftChangeRequest

User = get_user_model()
log = logging.getLogger()


def restrict_to_groups(*groups):
    def decorator(view):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.is_superuser or request.user.groups.filter(name__in=groups).exists():
                return view(request, *args, **kwargs)
            raise PermissionDenied

        return _wrapped_view

    return decorator


@login_required
def index(request):
    pending_shift_change_requests = ShiftChangeRequest.objects.filter(
        target__associated_person=request.user, approved=False
    )
    return render(request, "index.html", {"change_requests": pending_shift_change_requests})


@login_required
def user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_users_shifts = Shift.objects.filter(associated_person=target_user)
    target_users_shifts = [
        {
            "id": str(shift.id),
            "start": shift.start.isoformat(),
            "end": (shift.start + shift.duration).isoformat(),
            "title": str(shift),
            "allDay": False,
            "url": reverse("view_shift", args=(shift.id,)),
        }
        for shift in target_users_shifts
    ]
    target_users_shifts = json.dumps(target_users_shifts)
    return render(
        request,
        "users/user_profile.html",
        {"target_user": target_user, "target_users_shifts": target_users_shifts},
    )


@login_required
def edit_profile(request, user_id):
    if user_id != request.user.id:
        # TODO: let privileged users edit anyone's profile
        raise PermissionDenied
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            return HttpResponseRedirect(reverse("user_profile", args=(user_id,)))
    else:
        form = EditProfileForm(instance=user)
        return render(request, "users/edit_profile.html", {"user_id": user_id, "form": form})


@restrict_to_groups("Office staff", "Supervisors")
def create_user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = LRCDatabaseUser.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                password=form.cleaned_data["password"],
                si_course=form.cleaned_data["si_course"],
            )
            user.courses_tutored.set(form.cleaned_data["courses_tutored"])
            user.save()
            for group in form.cleaned_data["groups"]:
                group.user_set.add(user)
            return HttpResponseRedirect(reverse("user_profile", args=(user.id,)))
    else:
        form = CreateUserForm()
        return render(request, "users/create_user.html", {"form": form})


@restrict_to_groups("Office staff", "Supervisors")
def create_users_in_bulk(request):
    if request.method == "POST":
        form = CreateUsersInBulkForm(request.POST)
        assert form.is_valid()
        user_data = form.cleaned_data["user_data"]
        user_data = user_data.split("\n")
        user_data = [s.strip() for s in user_data]
        user_data = [s.split(",") for s in user_data]
        for username, email, first_name, last_name, primary_group, password in user_data:
            user = LRCDatabaseUser.objects.create_user(
                username=username, email=email, first_name=first_name, last_name=last_name, password=password
            )
            Group.objects.filter(name=primary_group).first().user_set.add(user)
        return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateUsersInBulkForm()
        return render(request, "users/create_users_in_bulk.html", {"form": form})


@restrict_to_groups("Office staff", "Supervisors")
def list_users(request, group):
    users = get_list_or_404(User.objects.filter(is_retired=False).order_by("last_name"), groups__name=group)
    return render(request, "users/list_users.html", {"users": users, "group": group})


@login_required
def view_shift(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    change_requests = ShiftChangeRequest.objects.filter(target=shift)
    return render(
        request,
        "shifts/view_shift.html",
        {"shift": shift, "change_requests": change_requests},
    )


@login_required
def new_shift_change_request(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    if shift.associated_person.id != request.user.id:
        # TODO: let privileged users edit anyone's shifts
        raise PermissionDenied
    if request.method == "POST":
        form = NewChangeRequestForm(request.POST)
        if form.is_valid():
            s = ShiftChangeRequest(
                target=shift, approved=False, approved_by=None, approved_on=None, **form.cleaned_data
            )
            s.save()
            return HttpResponseRedirect(reverse("view_shift", args=(shift_id,)))
    else:
        form = NewChangeRequestForm(
            initial={
                "new_associated_person": shift.associated_person,
                "new_start": shift.start,
                "new_duration": shift.duration,
                "new_location": shift.location,
            }
        )
        return render(
            request,
            "shifts/new_shift_change_request.html",
            {"shift_id": shift_id, "form": form},
        )


@login_required
def list_courses(request):
    courses = Course.objects.order_by("department", "number")
    return render(request, "courses/list_courses.html", {"courses": courses})


@login_required
def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    tutors = User.objects.filter(courses_tutored__in=(course,))
    sis = User.objects.filter(si_course=course)
    return render(
        request,
        "courses/view_course.html",
        {"course": course, "tutors": tutors, "sis": sis},
    )


@restrict_to_groups("Office staff", "Supervisors")
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            c = Course(**form.cleaned_data)
            c.save()
            return HttpResponseRedirect(reverse("view_course", args=(c.id,)))
    else:
        form = CourseForm()
        return render(request, "courses/add_course.html", {"form": form})


@restrict_to_groups("Office staff", "Supervisors")
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course.department = form.cleaned_data["department"]
            course.number = form.cleaned_data["number"]
            course.name = form.cleaned_data["name"]
            course.save()
            return HttpResponseRedirect(reverse("view_course", args=(course.id,)))
    else:
        form = CourseForm(
            initial={
                "department": course.department,
                "number": course.number,
                "name": course.name,
            }
        )
        return render(request, "courses/edit_course.html", {"form": form, "course_id": course.id})


@restrict_to_groups("Office staff", "Supervisors")
def view_shift_change_requests(request, kind):
    requests = get_list_or_404(ShiftChangeRequest, target__kind=kind, approved=False)
    return render(
        request,
        "scheduling/view_shift_change_requests.html",
        {"change_requests": requests, "kind": kind},
    )


@restrict_to_groups("Office staff", "Supervisors")
def view_shift_change_approved_requests(request, kind):
    requests = get_list_or_404(ShiftChangeRequest, target__kind=kind, approved=True)
    return render(
        request,
        "scheduling/view_approved_requests.html",
        {"change_requests": requests, "kind": kind},
    )


@restrict_to_groups("Office staff", "Supervisors")
def view_approved_request(request, kind, request_id):
    ap_request = ShiftChangeRequest.objects.get(request_id)
    return render(request, "scheduling/approved_request.html", {"ap_request": ap_request})


@restrict_to_groups("Office staff", "Supervisors")
def show_hardware(request):
    hardware = Hardware.objects.order_by("name")
    curLoans = Loan.objects.all()
    return render(
        request,
        "hardware/hardware_table.html",
        {"hardware": hardware, "curLoans": curLoans},
    )


@restrict_to_groups("Office staff", "Supervisors")
def show_loans(request):
    loanInfo = Loan.objects.order_by("return_time")

    return render(request, "loans/show_loans.html", {"loanInfo": loanInfo})


@restrict_to_groups("Office staff", "Supervisors")
def add_hardware(request):
    if request.method == "POST":
        form = AddHardwareForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        return HttpResponseRedirect(reverse("show_hardware"))
    else:
        form = AddHardwareForm()
        context = {"form": form}
    return render(request, "hardware/add_hardware.html", context)


@restrict_to_groups("Office staff", "Supervisors")
def add_loans(request):
    if request.method == "POST":
        form = NewLoanForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse("show_loans"))
    else:
        form = NewLoanForm()
    context = {"form": form}
    return render(request, "loans/add_loans.html", context)


@restrict_to_groups("Office staff", "Supervisors")
def edit_loans(request, loan_id):
    loan1 = Loan.objects.get(id=loan_id)
    if request.method == "POST":
        form = NewLoanForm(request.POST, instance=loan1)
        if form.is_valid():
            form.save()
            return redirect("show_loans")
    else:
        form = NewLoanForm(instance=loan1)

    return render(request, "loans/edit_loans.html", {"form": form, "loan_id": loan_id})


@restrict_to_groups("Office staff", "Supervisors")
def edit_hardware(request, hardware_id):
    hardware1 = Hardware.objects.get(id=hardware_id)
    if request.method == "POST":
        form = AddHardwareForm(request.POST, instance=hardware1)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("show_hardware")
    else:
        form = AddHardwareForm(instance=hardware1)
    context = {"form": form, "hardware_id": hardware_id}
    return render(request, "hardware/edit_hardware.html", context)
