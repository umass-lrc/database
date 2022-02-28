from django import forms
from django.forms import ModelForm

from .models import Hardware, Loan
from .widgets import DateTimePickerInput


class AddHardwareForm(ModelForm):
    class Meta:
        model = Hardware
        fields = ("name", "is_available")

        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class NewLoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = ("target", "hardware_user", "start_time", "return_time")

        widgets = {
            "target": forms.Select(attrs={"class": "form-control"}),
            "hardware_user": forms.Select(attrs={"class": "form-control"}),
            "start_time": DateTimePickerInput(),
            "return_time": DateTimePickerInput(),
        }
