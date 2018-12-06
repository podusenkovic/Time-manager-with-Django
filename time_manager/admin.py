from django.contrib import admin
from django.contrib.auth.models import User

from .models import Task
# Register your models here.

class TaskInline(admin.TabularInline):
    model = Task
    extra = 3

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Email',               {'fields' : ['email']}),
        ('Username',            {'fields' : ['username']}),
    ]
    list_display = ('username', 'email')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Task)
