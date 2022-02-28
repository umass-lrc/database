from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/<str:group>", views.list_users, name="list_users"),
    path("showHardware", views.show_hardware, name="showHardware"),
    path("addHardware", views.add_hardware, name="addHardware"),
    path("showLoans", views.show_loans, name="showLoans"),
    path("addLoans", views.add_loans, name="addLoans"),
    path("editLoans/<int:pk>", views.edit_loans, name="editLoans"),
]
