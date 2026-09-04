from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('assignments/', views.student_assignments, name='student_assignments'),
    path('classroom/<int:pk>/', views.classroom_detail, name='classroom_detail'),
]