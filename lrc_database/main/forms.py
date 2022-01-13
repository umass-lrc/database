from django.forms import forms
from .models import Hardware, Loan


class AddHardwareForm(forms.ModelForm):
    class meta:
        model = Hardware
        fields = ('name', 'is_available')


class NewLoanForm(forms.ModelForm):
    class meta:
        model = Loan
        fields = ('target', 'hardware_user', 'start_time', 'return_time')
