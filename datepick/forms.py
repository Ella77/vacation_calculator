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
from django_popup_view_field.fields import PopupViewField
from . popups import PopupView
import numpy

STATUS_CHOICES = (
    (1, "오전 반차"),
    (2, "오후 반차"),
)

CHOICES = (
    (1, "일반 대체"),
    (2, "매직 데이대체"),
)

class PromiseForm(forms.ModelForm):

    class Meta:
        model = Promise
        fields = ('start', 'end')
        widgets = {
            'start': forms.DateInput(attrs={'class': 'datetime-input',
                                            'style': 'border-color: blue;',
                                            'placeholder': '휴가 시작일'}),
            'end': forms.DateInput(attrs={'class': 'datetime-input',
                                          'style': 'border-color: red;',
                                          'placeholder': '휴가 끝나는 '}),

        }


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('jobstart',)
        widgets = {
            'jobstart': SelectDateWidget(years = range(timezone.now().year, 2000, -1))
        }


class HalfForm(forms.ModelForm):

    class Meta:
        model = Promise
        fields = ('start', 'status')
        widgets = {
            'start': forms.DateInput(attrs={'class': 'datetime-input',
                                            'style': 'border-color: blue;',
                                            'placeholder': '해당 날짜'}),
            'status': forms.Select(choices=STATUS_CHOICES),
        }

class ConfirmForm(forms.Form):
    color = PopupViewField(
        view_class=PopupView,
        popup_dialog_title='월차 사용일을 확인하세요.',
        required=True,
        help_text='공휴일 주의'
    )

class ReplaceForm(forms.ModelForm):
    class Meta :
        model = Promise
        fields = ('start', 'end', 'replace_day','replace_status')
        widgets = {
            'start' : forms.DateInput(attrs={'class': 'datetime-input',
                                            'style': 'border-color: blue;',
                                            'placeholder': '대체근무했던 시작날'}),
            'end': forms.DateInput(attrs={'class': 'datetime-input',
                                          'style': 'border-color: red;',
                                          'placeholder': '대체근무했던 끝나는 날'}),
            'replace_status': forms.Select(choices=CHOICES),
           'replace_day' : forms.NumberInput(attrs={'placeholder':'휴가로 얻을 일'}),
        }

