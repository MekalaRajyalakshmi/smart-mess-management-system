from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.register_view, name='home'),
    path('register/', views.register_view, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/student/', views.studentdashboard, name='studentdashboard'),
    path('dashboard/cook/', views.cookdashboard, name='cookdashboard'),
    path('dashboard/rep/', views.repsdashboard, name='repsdashboard'),
]