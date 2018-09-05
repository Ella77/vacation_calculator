from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from .models import Vacation, Employee, VacationHistory
# # Create your views here.
# from .models import
from .forms import  VacationForm, EmployeeForm, HalfForm, ReplaceForm, SpecialForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .calculate import Calculate_Total_Vacation_Until_This_Year,Calculate_This_Year_Vacation,Calculate_Passed_Days
import datetime
import numpy
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from pygal.style import DarkStyle
from .charts import VacationChart
from .forms import ConfirmForm
from django.http import HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import date
from datetime import timedelta
from django.views.generic.edit import UpdateView
from .mailsystem import *
from django.views import generic
from chartit import DataPool,Chart
from django_slack import slack_message

class IndexView(TemplateView):
    template_name = 'datepick/base.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)


        vacation = VacationChart(
        height = 1000,
        width = 600,
        style = DarkStyle,

    )
        context['vacation'] = vacation.generate()
        return context

def chart(request):
    data = \
        DataPool(
            series =
            [{ 'options': {
                'source': VacationHistory.objects.all()},

                'terms':[
                    'user',
                    {'총 연차': 'total'},
                    {'올해 남은 연차': 'thisyear_left'},
                    {'올해 사용량': 'thisyear_used'},
                    {'올해 대체휴가': 'replace_workday'},
                    {'올해 특별휴가': 'special_day'},

                ]}])
    cht = Chart(
        datasource = data,
        series_options =
        [{'options':{
            'type':'column',
            'stacking':False},

            'terms':{
                'user':[

                    '총 연차',
                    '올해 남은 연차',
                    '올해 사용량',
                    '올해 대체휴가',
                    '올해 특별휴가',
                ]
        }}],
        chart_options =
        {'title': {
            'text': '사용자별 휴가와 사용현황'
        },

            'xAxis': {
                'title': {
                    'text': '사용자',
                }},
            'yAxis': {
                'title': {
                    'text': 'vacation',
                }
            }})

    return render(request,'chart.html',{'vacationchart':cht})

class VacationListbyAuthor(generic.ListView):

    model = Vacation
    paginate_by = 5
    template_name = 'datepick/vacation_list_by_author.html'

    def get_queryset(self):

        return Vacation.objects.filter(author_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(VacationListbyAuthor,self).get_context_data(**kwargs)

        context['vacationer']= get_object_or_404(Employee,pk=self.kwargs['pk'])
        return context


class VacationerListView(generic.ListView):
    model = Employee
    paginate_by = 5
    template_name = 'datepick/employee_list.html'


class VacationUpdate(UpdateView):
    model = Vacation
    fields = '__all__'
    template_name = "edit_entry.html"
    #
    # def form_valid(self,form) :
    #
    #      context = self.get_context_data(form=form)
    #      user= form.save()
    #      if user.status == 0 :
    #          general = context['form_general']


    def get_form_class(self):
        self.object = Vacation.objects.get(pk=self.kwargs['pk'])
        if self.object.status in [0,4,5] :
            return ReplaceForm
        else :
            return HalfForm
    def get_success_url(self):
        if self.request.user.is_superuser :
            return reverse('list_admin')
        else :
            reverse('list')

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            self.object = Vacation.objects.get(pk=self.kwargs['pk'])
            if self.request.user.is_superuser:
                self.object.bus_day_count = post.bus_day_count

                if self.object.status in [4, 5]:
                    self.object.regi_status = True
            else :
                if self.object.status in [0, 4]:
                    Vacation.calc_bus_day(post)
                if self.object.status in [4, 5]:
                    self.object.regi_status = False

            post.save()
            vacationhistory, created = VacationHistory.objects.update_or_create(user=self.request.user)
            VacationHistory.get_data(vacationhistory)
            if self.request.user.is_superuser:
                return redirect('list_admin')
            else :
                return redirect('list')

edit = VacationUpdate.as_view()



@staff_member_required
def approve(request,pk):
    post = get_object_or_404(Vacation, pk=pk)
    post.approve()
    vacationhistory, created = VacationHistory.objects.update_or_create(user=request.user)
    VacationHistory.get_data(vacationhistory)
    slack_message('post/viewed.slack',{
        'post':post,
        'user':request.user,
    })
    return redirect('list_admin')

# def base(request):
#     return render(request,'datepick/base.html')
@login_required
def post_new(request):
    return render(request, 'datepick/post_new.html')

@login_required
def post_new_full(request):
    if request.method=="POST":

        form = VacationForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            post = form.save(commit =False)
            post.author = request.user
            Vacation.calc_bus_day(post)

            post.save()
            vacationhistory, created = VacationHistory.objects.update_or_create(user=request.user)
            VacationHistory.get_data(vacationhistory)
            return redirect ('list')
    else :
            form = VacationForm()
    return render(request, 'datepick/new_full.html', {'form' : form}, )



@login_required
def post_new_half(request):
    if request.method == "POST":
        form = HalfForm(request.POST, is_staff=False)
        form.instance.author = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.end = post.start
            if post.status ==1 :
             post.bus_day_count = 1
            else :
                post.bus_day_count = 0.5

            post.save()
            vacationhistory, created = VacationHistory.objects.update_or_create(user=request.user)
            VacationHistory.get_data(vacationhistory)
            return redirect('list')
    else:
        form = HalfForm(is_staff=False)

    return render(request, 'datepick/new_half.html', {'form':form}, )

@login_required
def main(request):
    test()

    data = \
        DataPool(
            series=
            [{'options': {
                'source': VacationHistory.objects.filter(user=request.user)},
                'terms': [
                    'user',
                    {'총 연차':'total'},
                    {'올해 남은 연차':'thisyear_left'},
                    {'올해 사용량':'thisyear_used'},
                    {'올해 대체휴가':'replace_workday'},
                        {'올해 특별휴가':'special_day'},
                ]}
            ])
    cht = Chart(
        datasource=data,
        series_options=
        [{'options': {
            'type': 'bar',
            'stacking': False},

            'terms': {
                'user': [

                    '총 연차',
                    '올해 남은 연차',
                    '올해 사용량',
                    '올해 대체휴가',
                    '올해 특별휴가',
                ]
            }}],
        chart_options=
        {'title': {
            'text': '사용자별 휴가와 사용현황'
        },

            'xAxis': {
                'title': {
                    'text': '사용자',
                }},
            'yAxis':{
                'title':{
                    'text':'vacation',
                }
            } })



    if Employee.objects.filter(users = request.user).exists() == False:
        return redirect('setting')

    else:

        latestjobstart = Employee.objects.filter(users= request.user).last()
        thisyear_available = latestjobstart.get_current_vacation()
        workingdays_with = latestjobstart.get_keep()
        total_available = round(Calculate_Total_Vacation_Until_This_Year(latestjobstart.jobstart), 1)
        lastyear_available = total_available-thisyear_available
        thisyear_used = 0
        replace_workday = 0
        special_day = 0

        queryset = Vacation.objects.filter(author=request.user)
        queryset = queryset.filter(Q(Q(start__year=timezone.now().year) | Q(end__year=timezone.now().year)))
        queryset = queryset.filter(regi_status=True)
        for final in queryset:
            if final.status == 4:
                special_day += final.bus_day_count
            elif final.status == 5 :
                replace_workday += final.bus_day_count
            elif (final.status == 0):
                if final.start.year == final.end.year :
                 thisyear_used += final.bus_day_count
                else :
                  if final.start.year == timezone.now().year :
                    end_of_year = date(final.start.year,12,31)
                    thisyear_used += numpy.busday_count(final.start,end_of_year+timedelta(1))
                  else :
                    start_of_year = date(final.end.year,1,1)
                    thisyear_used += numpy.busday_count(start_of_year,final.end+timedelta(1))
            else :
                thisyear_used += final.bus_day_count
        thisyear_origin_left = thisyear_available-thisyear_used

        thisyear_left = thisyear_available-thisyear_used+replace_workday
        # VacationHistory.save(post)
        # vacation_history = VacationHistory(user=request.user, thisyear_left)
        return render(request, 'datepick/main.html', {'vacation':cht, 'latestjobstart':latestjobstart, 'thisyear_origin_left':thisyear_origin_left, 'lastyear_available':lastyear_available, 'thisyear_used':thisyear_used, 'workingdays_with':workingdays_with,
                                                      'replace_workday':replace_workday, 'special_day':special_day, 'thisyear_left':thisyear_left, })


def list(request):
        forms = Vacation.objects.filter(Q(author=request.user) & Q(start__year =timezone.now().year) & Q(end__year=timezone.now().year)).order_by('start')
        return render (request, 'datepick/list.html', {'forms': forms}, )


def list_admin(request):

        members = User.objects.all()
        unsolved = Vacation.objects.filter(Q(regi_status = 0) & Q(start__year =timezone.now().year) & Q(end__year=timezone.now().year)).order_by('-created_time')
        qs = Vacation.objects.all()
        q = request.GET.get('q','')
        if q:
            qs=qs.filter(Q(author__username__contains=q)& Q(start__year =timezone.now().year) & Q(end__year=timezone.now().year))


        #
        # forms = Promise.objects.filter(Q(start__year=timezone.now().year) | Q(end__year=timezone.now().year)).order_by(
        #     'start')
        return render(request, 'datepick/list_admin.html', {'unsolved':unsolved,'qs':qs, 'q':q, 'members':members, },)


def list_user(request, pk):
    name = User.objects.get(id=pk)
    forms = Vacation.objects.filter(Q(author_id =pk) & Q(Q(start__year=timezone.now().year) | Q(end__year=timezone.now().year))).order_by(
            '-start')
    source = VacationHistory.objects.filter(user_id=pk)
    data = \
        DataPool(
            series=
            [{'options': {
                'source': source}
                ,
                'terms': [
                    'user',
                    {'총 연차': 'total'},
                    {'올해 남은 연차': 'thisyear_left'},
                    {'올해 사용량': 'thisyear_used'},
                    {'올해 대체휴가': 'replace_workday'},
                    {'올해 특별휴가': 'special_day'},
                ]}
            ])
    cht = Chart(
        datasource=data,
        series_options=
        [{'options': {
            'type': 'bar',
            'stacking': False},

            'terms': {
                'user': [
                    '총 연차',
                    '올해 남은 연차',
                    '올해 사용량',
                    '올해 대체휴가',
                    '올해 특별휴가',
                ]
            }}],
        chart_options=
        {'title': {
            'text': '사용자별 휴가와 사용현황'
        },

            'xAxis': {
                'title': {
                    'text': 'user',
                }},
            'yAxis': {
                'title': {
                    'text': 'vacation',
                }
            }})

    return render(request, 'datepick/list_user.html', {'vacationchart':cht,'forms': forms, 'name':name})


@login_required
def post_edit(request,pk):
    # post = get_object_or_404(Promise, pk=pk)
    #
    # def post_get( post ):
    #         if post.status == 0 :
    #             form = PromiseForm(request.POST, instance=post)
    #             return form
    #         if post.status == 4:
    #             form = SpecialForm(request.POST, instance=post)
    #             return form
    #         if post.status == 5 :
    #             form = ReplaceForm(request.POST, instance=post)
    #             return form
    #         else :
    #             form = HalfForm(request.POST,instance=post, is_staff=False)
    #             return form
    #
    # if request.method == "POST":
    #     form = post_get( post)
    #     if form.is_valid():
    #         post = form.save(commit = False)
    #         post.author = request.user
    #         post.save()
    #         if request.user.is_superuser:
    #             return redirect('list_admin')
    #         else :
    #             return redirect('list')
    #
    # return render(request, 'datepick/edit.html', {'form': form})
    return render(request, 'edit_entry.html')
@login_required
def post_remove(request,pk):
    post = get_object_or_404(Vacation, pk=pk)

    post.delete()
    vacationhistory, created = VacationHistory.objects.update_or_create(user=request.user)
    VacationHistory.get_data(vacationhistory)
    if request.user.is_superuser:
        return redirect('list_admin')
    else:
        return redirect('list')


def help(request):
    return render(request, 'datepick/help.html')


def setting(request):

    if request.method == "POST":
        form = EmployeeForm(request.POST)

        if form.is_valid():
            jobstart = form.cleaned_data.get('jobstart')
            # if Employee.DoesNotExist :
            #     post = form.save(commit=False)
            #     post.users = request.user
            #     post.save()
            employee = Employee.objects.get(users=request.user)
            employee.jobstart = jobstart
            employee.save()
        return redirect('main')
    else:
        form = EmployeeForm()

    return render(request, 'datepick/setting.html', {'form': form})
#
# def
#     Promise.end-Promise.start




def replace_new(request):

    form = ReplaceForm()
    if request.method == "POST":
        form = ReplaceForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():


            post = form.save(commit=False)
            post.author = request.user
            post.status = 5
            if request.user.is_superuser:
                post.regi_status = True
            else :
                post.regi_status = False

            post.save()
            vacationhistory, created = VacationHistory.objects.update_or_create(user=request.user)
            VacationHistory.get_data(vacationhistory)
            return redirect('list')


    return render(request, 'datepick/post_replace.html', {'form': form}, )


def base(request):
    return render(request,'datepick/base.html')


def post_full(request):
    return render(request,'datepick/post_full.html')


@login_required
def post_new_year_full(request):
    if request.method == "POST":
        form = VacationForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            Vacation.calc_bus_day(post)

            post.save()
            vacationhistory, created = VacationHistory.objects.update_or_create(user=request.user)
            VacationHistory.get_data(vacationhistory)
            return redirect('list')
    else:
        form = VacationForm()

    return render(request, 'datepick/post_new_year_full.html', {'form':form},)

def confirm(request):

    return render(request,'datepick/confirm.html')


def post_special(request):
    return render(request, 'datepick/post_special.html', )


def post_special_new(request):
        # instead of hardcoding a list you could make a query of a model, as long as
        # it has a __str__() method you should be able to display it.

        if request.method == "POST":
            form = SpecialForm(request.POST)
            form.instance.author = request.user
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user

                post.status = 4
                if request.user.is_superuser:
                    post.regi_status = True
                else:
                    post.regi_status = False

                Vacation.calc_bus_day(post)

                post.save()
                vacationhistory, created = VacationHistory.objects.update_or_create(user=request.user)
                VacationHistory.get_data(vacationhistory)
                return redirect('list')
        else:
            form = SpecialForm()

        return render(request, 'datepick/post_special_new.html', {'form': form}, )