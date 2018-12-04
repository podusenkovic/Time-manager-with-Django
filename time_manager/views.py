from django.shortcuts import render, redirect
from django.views import generic
from .models import CustomUserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate
# Create your views here.

def IndexView(request):
    template_name = 'time_manager/index.html'
    return render(request, template_name)

class AccountView(generic.ListView):
    template_name = 'time_manager/account.html'
    def get_queryset(request):
        pass


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('time_manager:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'time_manager/signup.html', {'form' : form})


def signin(request):
    if request.method == 'POST':
        print(request.POST.get('username'))
        user = authenticate(username = request.POST.get('username'),
                            password = request.POST.get('password'))
        if user:
            return HttpResponseRedirect(reverse('time_manager:account', args = (request.POST['username'],)))
        else:
            return render(request, 'time_manager/index.html',
                          {'error_message' : "No user or bad pass!"})
