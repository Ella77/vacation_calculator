from django.shortcuts import render, redirect, get_object_or_404
from .models import Promise, Employee
# # Create your views here.
# from .models import Promise
from .forms import  PromiseForm, EmployeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .calculate import Calculate,Calculate_year,duration
import datetime


# def base(request):
#     return render(request,'blog/base.html')


@login_required
def post_new(request):
    if request.method=="POST":
        form = PromiseForm(request.POST)
        if form.is_valid():
            post = form.save(commit =False)
            post.author = request.user

            post.save()

            return redirect ('list')
    else :
            form = PromiseForm()

    return render(request, 'blog/pick.html', {'form' : form}, )

@login_required
def main(request):
    if Employee.objects.exists()== False:
        return redirect('setting')

    else :

        latest = Employee.objects.last()
        b = round(Calculate(latest.jobstart),1)
        d = round(Calculate_year(latest.jobstart),1)
        p= b-d
        dur = 0
        for final in Promise.objects.all():
            dur += duration(final.end,final.start)
        return render(request, 'blog/main.html',{'latest':latest, 'd':d, 'p':p, 'dur':dur},)


def list(request):
    if request.user.is_superuser :
        forms =Promise.objects.order_by('start')
    else :
        forms = Promise.objects.filter(author=User.objects.get(username=request.user.get_username())).order_by('start')

    return render (request,'blog/list.html', {'forms': forms}, )

@login_required
def post_edit(request,pk):
    post = get_object_or_404(Promise, pk=pk)
    if request.method == "POST" :
        form = PromiseForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('list')
    else:
        form = PromiseForm(instance = post)
    return render(request, 'blog/edit.html',{'form':form})

@login_required
def post_remove(request,pk):
    post = get_object_or_404(Promise, pk=pk)
    post.delete()
    return redirect('list')

def help(request):
    return render(request,'blog/help.html')


def setting(request):

    if request.method == "POST":
        form = EmployeeForm(request.POST)


        if form.is_valid():
            jobstart = form.cleaned_data.get('jobstart')
            if Employee.DoesNotExist :
                post = form.save(commit=False)
                post.users = request.user
                post.save()
            else :
                employee = Employee.objects.get(users=request.user)
                employee.jobstart = jobstart
                employee.save()
            return redirect('main')
    else:
        form = EmployeeForm()

    return render(request, 'blog/setting.html', {'form':form})
#
# def
#     Promise.end-Promise.start