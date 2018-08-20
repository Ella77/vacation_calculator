from django import forms
from django.forms import ModelForm
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.timezone import timedelta
from .models import Promise, Employee
from django.forms.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from django.utils import timezone
from django.utils.dates import MONTHS





class PromiseForm(forms.ModelForm):






    class Meta:
        model = Promise
        fields= ('start','end',)
        widgets = {
            'start':forms.DateInput(attrs={'class':'datetime-input', 'style': 'border-color: blue;','placeholder':'휴가 시작일',}),
            'end':forms.DateInput(attrs={'class':'datetime-input', 'style':'border-color: red;','placeholder':'휴가 끝나는 ',}),

        }
class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('jobstart',)
        widgets = {
            'jobstart': SelectDateWidget(years =range(2000,timezone.now().year),)
        }
