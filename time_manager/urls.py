from django.urls import path
from . import views

app_name = 'time_manager'
urlpatterns = [
    path('', views.IndexView, name = 'index'),
    path('signup/', views.signup, name = 'signup'),
    path('signin/', views.signin, name = 'signin'),
    path('<slug:username>/account/', views.AccountView.as_view(), name = 'account')
]
