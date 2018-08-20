from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import timedelta
import datetime

from django.contrib.auth.models import User

class Promise(models.Model):
    start = models.DateField()
    end = models.DateField()
    created_time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Employee(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    jobstart= models.DateField()


    # def check_overlap(self, fixed_start,fixed_end,new_start,new_end):
    #     overlap = False
    #     if new_start == fixed_end or new_end == fixed_start:  # edge case
    #         overlap = False
    #     elif (new_start >= fixed_start and new_start <= fixed_end) or (
    #             new_end >= fixed_start and new_end <= fixed_end):  # innner limits
    #         overlap = True
    #     elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
    #         overlap = True
    #
    #     return overlap
    #
    #
    # def clean(self):
    #     if self.end < self.start :
    #         raise ValidationError('시작날 이후 날짜를 선택해주세요')
    #
    #     # events = Event.objects.filter(day=self.start_time)
    #
    #     events = Promise.objects.filter(start_time =self.start)
    #     if events.exists():
    #         for event in events :
    #             if self.check_overlap(event.start,event.end,self.start,self.end) :
    #                 raise ValidationError(
    #                     '휴가 날짜가 겹칩니다' +str(event.start_time) + '-' +str(event.end_time)
    #                 )