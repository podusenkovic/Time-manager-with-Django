from django.urls import path
from . import views

app_name = 'time_manager'
urlpatterns = [
    path('', views.IndexView, name = 'index'),
    path('signup/', views.signup_view, name = 'signup'),
    path('signin/', views.signin_view, name = 'signin'),
    path('logout/', views.logout_view, name = 'logout'),
    path('<slug:username>/', views.AccountView, name = 'account'),
    path('<slug:username>/task_<int:task_id>_change/', views.task_changeView, name = 'task_change'),
    path('<slug:username>/create_task/', views.task_createView, name = 'task_create'),
]
