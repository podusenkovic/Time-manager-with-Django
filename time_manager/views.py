from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import CustomUserCreationForm, TaskCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.dateparse import parse_datetime

from datetime import datetime
from .models import Task

from django.contrib.auth import authenticate
# Create your views here.

def IndexView(request):
    template_name = 'time_manager/index.html'
    return render(request, template_name)

def task_changeView(request, username, task_id):
    if not request.user.is_authenticated or not request.user.username == username:
        return render(request, 'time_manager/index.html', {'error_message' : 'not logged in'})
    else:
        task = get_object_or_404(Task, pk = task_id)
        if task.user.username == username:
            if request.method == 'POST':
                if not request.POST.get('deleteTask'):
                    task.task_text = request.POST.get('newTaskText')
                    task.task_start_date = parse_datetime(request.POST.get('newTaskDate'))#, '%Y-%m-%d %H:%M')
                    task.save()
                else:
                    task.delete()
                #return render(request, 'time_manager/account.html')
                return HttpResponseRedirect(reverse('time_manager:account', args = (username,)))
            else:
                return render(request, 'time_manager/task_change.html', {'user' : request.user, 'task' : task})
        else:
            return render(request, 'time_manager/index.html', {'error_message' : 'its not your task'})


def task_createView(request, username):
    if not request.user.is_authenticated or not request.user.username == username:
        return render(request, 'time_manager/index.html', {'error_message' : 'not logged in'})
    else:
        if request.method == 'POST':
            form = TaskCreationForm(request.POST)
            if form.is_valid():
                form.save(username)
                return render(request, 'time_manager/account.html')
        else:
            form = TaskCreationForm()
            return render(request, 'time_manager/task_create.html', {'user' : request.user, 'form' : form})

def AccountView(request, username):
    template_name = 'time_manager/account.html'
    if not request.user.is_authenticated or not request.user.username == username:
        return render(request, 'time_manager/index.html', {'error_message' : 'not logged in'})
    else:
        return render(request, template_name)


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('time_manager:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'time_manager/signup.html', {'form' : form})


def signin_view(request):
    if request.method == 'POST':
        user = authenticate(username = request.POST.get('username'),
                            password = request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('time_manager:account', args = (request.POST['username'],)),
                                        {'user' : user})
        else:
            return render(request, 'time_manager/index.html',
                          {'error_message' : "No user or bad pass!"})

def logout_view(request):
    logout(request)
    return render(request, 'time_manager/index.html',
                  {'error_message' : "Succesfull logout"})
