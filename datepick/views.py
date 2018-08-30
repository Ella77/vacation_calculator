from django.shortcuts import render, redirect, get_object_or_404
from .models import Promise, Employee
# # Create your views here.
# from .models import Promise
from .forms import  PromiseForm, EmployeeForm, HalfForm, ReplaceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .calculate import Calculate,Calculate_year,Calculate_keep
import datetime
import numpy
from django.views.generic import FormView
from .forms import ConfirmForm
from django.http import HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import date
from datetime import timedelta
from .mailsystem import *



# def base(request):
#     return render(request,'datepick/base.html')
@login_required
def post_new(request):
    return render(request, 'datepick/post_new.html')

@login_required
def post_new_full(request):
    if request.method=="POST":
        form = PromiseForm(request.POST)

        if form.is_valid():
            post = form.save(commit =False)
            post.author = request.user
            Promise.calc_bus_day(post)
            post.save()

            return redirect ('list')
    else :
            form = PromiseForm()
    return render(request, 'datepick/new_full.html', {'form' : form}, )



@login_required
def post_new_half(request):
    if request.method == "POST":
        form = HalfForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.end = post.start

            post.save()

            return redirect('list')
    else:
        form = HalfForm()

    return render(request, 'datepick/new_half.html', {'form':form}, )

@login_required
def main(request):

    if Employee.objects.filter(users = request.user).exists() == False:
        return redirect('setting')

    else:

        latest = Employee.objects.last()

        d = latest.get_current_vacation()
        keep = latest.get_keep()
        b = round(Calculate(latest.jobstart), 1)
        p = b-d
        dur = 0
        replace = 0

        for final in Promise.objects.filter( Q(start__year=timezone.now().year)|Q(end__year =timezone.now().year)& Q(author=request.user)):
            if  (final.replace_status !=0):
                replace += final.replace_day
            elif (final.status!=0):
                    dur += 0.5
            else:
                if final.start.year == final.end.year :
                 dur += numpy.busday_count(final.start, final.end+timedelta(1))
                else :
                  if final.start.year == timezone.now().year :
                    end_of_year = date(final.start.year,12,31)
                    dur += numpy.busday_count(final.start,end_of_year+timedelta(1))
                  else :
                    start_of_year = date(final.end.year,1,1)
                    dur += numpy.busday_count(start_of_year,final.end+timedelta(1))
        used = d-dur+replace

        return render(request, 'datepick/main.html', {'latest':latest, 'used': used, 'p':p, 'dur':dur, 'keep':keep,
                                                      'replace':replace,})


def list(request):
        forms = Promise.objects.filter(Q(author=request.user)| Q(start__year =timezone.now().year) | Q(end__year=timezone.now().year)).order_by('start')
        return render (request, 'datepick/list.html', {'forms': forms}, )

def list_admin(request):
    if request.user.is_superuser:
        forms = Promise.objects.filter(Q(start__year=timezone.now().year) | Q(end__year=timezone.now().year)).order_by(
            'start')
        return render(request, 'datepick/list_admin.html', {'forms': forms}, )

@login_required
def post_edit(request,pk):
    post = get_object_or_404(Promise, pk=pk)
    if request.method == "POST" :
        form = PromiseForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            if request.user.is_superuser:
                return redirect('list_admin')
            else :
                return redirect('list')
    else:
        form = PromiseForm(instance = post)
    return render(request, 'datepick/edit.html', {'form':form})

@login_required
def post_remove(request,pk):
    post = get_object_or_404(Promise, pk=pk)
    post.delete()
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

        if form.is_valid():


            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('list')


    return render(request,'datepick/replace_new.html',{'form': form},)


def base(request):
    return render(request,'datepick/base.html')


def post_full(request):
    return render(request,'datepick/post_full.html')


@login_required
def post_new_year_full(request):
    if request.method == "POST":
        form = PromiseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('list')
    else:
        form = PromiseForm()

    return render(request, 'datepick/post_new_year_full.html', {'form':form},)

def confirm(request):

    return render(request,'datepick/confirm.html')