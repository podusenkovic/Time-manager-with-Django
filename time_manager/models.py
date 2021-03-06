import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


class Task(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
    task_text = models.CharField(max_length = 200)
    task_start_date = models.DateTimeField('date start')
    def create_task(self, task_text, task_start_date):
        book = self.create(task_text = task_text, task_start_date = task_start_date)
        return book

    def __str__(self):
        return self.task_text

    def start_soon(self):
        now = timezone.now()
        return datetime.timedelta(days = 0) <= self.task_start_date - now <= datetime.timedelta(days = 1)


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label = 'Enter username', min_length = 4, max_length = 150,
                widget = forms.TextInput(attrs={'placeholder': 'Username',
                                                'class' : 'form-control'}))
    email = forms.EmailField(label = 'Enter email',
                widget = forms.TextInput(attrs={'placeholder': 'Email',
                                                'class' : 'form-control',
                                                'type' : 'email'}))
    password1 = forms.CharField(label = 'Enter password',
                widget = forms.TextInput(attrs={'placeholder': 'Password',
                                                'class' : 'form-control',
                                                'type' : "password"}))
    password2 = forms.CharField(label = 'Confirm password',
                widget = forms.TextInput(attrs={'placeholder': 'Confirm password',
                                                'class' : 'form-control',
                                                'type' : "password"}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username = username)
        if r.count():
            raise ValidationError("Username already in use!")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email = email)
        if r.count():
            raise ValidationError("Email already in use!")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesn't match!")
        return password2

    def save(self, commit = True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user;

class TaskCreationForm(forms.Form):
    task_text = forms.CharField(label = 'Enter text of the task', min_length = 4, max_length = 150,
                                widget = forms.TextInput(attrs={'placeholder': 'Task text',
                                                                'class' : 'form-control'}))
    task_date = forms.DateTimeField(widget = forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}))

    def clean_task_text(self):
        task_text = self.cleaned_data['task_text'].lower()
        return task_text

    def clean_task_date(self):
        task_date = self.cleaned_data['task_date']
        return task_date

    def save(self, username, commit = True):
        task = Task(
            user = User.objects.get(username = username),
            task_text = self.cleaned_data['task_text'],
            task_start_date = self.cleaned_data['task_date']
        )
        task.save()
