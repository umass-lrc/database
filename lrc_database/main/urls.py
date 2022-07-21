from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("courses/", views.list_courses, name="list_courses"),
    path("courses/<int:course_id>", views.view_course, name="view_course"),
    path("courses/<int:course_id>/edit", views.edit_course, name="edit_course"),
    path("courses/add", views.add_course, name="add_course"),
    path(
        "scheduling/shift_change_requests/<str:kind>",
        views.view_shift_change_requests,
        name="view_shift_change_requests",
    ),
    path(
        "scheduling/approved_change_requests/<str:kind>",
        views.view_shift_change_approved_requests,
        name="view_approved_change_requests",
    ),
    path(
        "scheduling/approved_change_requests/<int:request_id>",
        views.view_shift_change_approved_requests,
        name="view_approved_request",
    ),
    path(
        "scheduling/shift_change_requests/<str:kind>/<int:request_id>",
        views.view_shift_change_approved_requests,
        name="view_request",
    ),
    path("shifts/<int:shift_id>", views.view_shift, name="view_shift"),
    path(
        "shifts/<int:shift_id>/request_change",
        views.new_shift_change_request,
        name="new_shift_change_request",
    ),
    path("users/<int:user_id>", views.user_profile, name="user_profile"),
    path("users/<int:user_id>/edit", views.edit_profile, name="edit_profile"),
    path("users/<str:group>", views.list_users, name="list_users"),
    path("show_hardware", views.show_hardware, name="showHardware"),
    path("show_loans", views.show_loans, name="showLoans"),
    path("edit_loans/<int:loan_id>", views.edit_loans, name="edit_loans"),
    path("edit_hardware/<int:hardware_id>", views.edit_hardware, name="edit_hardware"),
    path("add_hardware", views.add_hardware, name="add_hardware"),
    path("add_loans", views.add_loans, name="add_loans"),
    path("users/create", views.create_user, name="create_user"),
    path("users/create/bulk", views.create_users_in_bulk, name="create_users_in_bulk"),
    path("users/groups/<str:group>", views.list_users, name="list_users"),
]
