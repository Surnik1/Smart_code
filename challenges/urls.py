from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    
    # 1. Сначала должен идти роут создания (конкретная ссылка)
    path('task/create/', views.create_task, name='create_task'),
    path('history/', views.submission_history, name='submission_history'),

    # AI API endpoints
    path('api/ai/generate-task/', views.api_generate_task, name='api_generate_task'),
    path('api/ai/<slug:slug>/hint/', views.api_code_hint, name='api_code_hint'),
    path('api/ai/<slug:slug>/review/', views.api_code_review, name='api_code_review'),

    # 2. И только потом динамический slug (любой другой текст)
    path('task/<slug:slug>/', views.task_detail, name='task_detail'),
]