from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="index"), path('showHardware', views.show_hardware, name='showHardware'),
               path('addHardware', views.add_hardware, name='addHardware'),
               path('showLoans', views.show_loans, name='showLoans')]
