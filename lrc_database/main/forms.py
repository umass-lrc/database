from django.forms import ModelForm

from .models import Hardware, Loan


class AddHardwareForm(ModelForm):
    class meta:
        model = Hardware
        fields = ('name', 'is_available')


class NewLoanForm(ModelForm):
    class meta:
        model = Loan
        fields = ('target', 'hardware_user', 'start_time', 'return_time')
