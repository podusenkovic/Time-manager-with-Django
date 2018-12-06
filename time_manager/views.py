from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import CustomUserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Task

from django.contrib.auth import authenticate
# Create your views here.

def IndexView(request):
    template_name = 'time_manager/index.html'
    return render(request, template_name)

def task_changeView(request, username, task_id):
    if not request.user.is_authenticated or not request.user.username == username:
        task = get_object_or_404(Task, pk = task_id)
        return render(request, 'time_manager/index.html', {'error_message' : 'not logged in'})
    else:
        return render(request, 'time_manager/task_change.html', {'task' : task})



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
