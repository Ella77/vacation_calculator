from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from .calculate import Calculate,Calculate_year,Calculate_keep
from django.contrib.auth.models import User
from datetime import date, timedelta
import numpy
from django.db.models import Q

STATUS_CHOICES = (
    (1, "풀타임"),
    (2, "오전 반차"),
    (3, "오후 반차"),

)

SELECT_REASON = (
    ('매직데이', "매직데이"),

)


class Promise(models.Model):
    start = modaddadels.DateField(blank = False)
    end = models.DateField(default=start)
    bus_day_count = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    replace_day =models.FloatField(default =0.0)
    reason = models.CharField(choices= SELECT_REASON, max_length=100)


    def calc_bus_day(self):

        self.bus_day_count = numpy.busday_count(self.start, self.end+timedelta(1))

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = True
        elif (fixed_start <= new_start <= fixed_end) \
                or (fixed_start <= new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def check_overlap_half(self, fixed_start, fixed_status, new_start, new_status):
        overlap = False
        if (fixed_start == new_start) & (fixed_status ==1 ):
            overlap = True
        if (fixed_start == new_start) & (fixed_status == new_status) :
            overlap = True
        return overlap



    def clean(self):
        if self.status != 0 :
            events = Promise.objects.filter(status=1 or 2 or 3)
            if events.exists():
                for event in events:
                    if self.check_overlap_half(event.start,event.status,self.start,self.status):
                        if event.status == 1:
                            raise ValidationError(str(event.start)+' 일 풀타임으로 이미 신청')
                        elif event.status == 2:
                            raise ValidationError(str(event.start)+' 일 오전 반차로 이미 신청')
                        elif event.status == 3  :
                            raise ValidationError(str(event.start)+' 일 오후 반차로 이미 신청')
                        else :
                            raise ValidationError(
                                str(event.start) + '-' + str(event.end) + '특별 휴가로 이미 신청한 날짜에요')
        else :

            if self.end < self.start:
                raise ValidationError('시작일 이후 날짜를 설정해주세요')

            events = Promise.objects.filter(status=0)
            if events.exists():
                for event in events:
                    if self.check_overlap(event.start, event.end, self.start, self.end):
                        if event.replace_day ==0 :


                            raise ValidationError(
                                 str(event.start) + '-' + str(event.end)+ '일반 휴가로 이미 신청한 날짜에요')
                        else :
                            raise ValidationError(
                                 str(event.start) + '-' + str(event.end) + '대체 휴가로 이미 신청한 날짜에요')


class VacationHistory(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    total = models.FloatField(default=0.0)
    used = models.FloatField(default=0.0)
    available = models.FloatField(default=0.0)
    created = models.DateTimeField(default=timezone.now)


class Employee(models.Model):
    users = models.OneToOneField(User, related_name='employee', on_delete=models.CASCADE)
    jobstart = models.DateField()


    def get_current_vacation(self):
        return round(Calculate_year(self.jobstart), 1)

    def get_keep(self):
        return round(Calculate_keep(self.jobstart), 1)



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
