from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('task/create/', views.create_task, name='create_task'),
    path('history/', views.submission_history, name='submission_history'),

    # Аналитика учителя
    path('classes/<int:class_id>/analytics/', views.classroom_analytics, name='classroom_analytics'),
    path('classes/<int:class_id>/export-csv/', views.export_classroom_csv, name='export_classroom_csv'),

    # Code Battle (Дуэли 1 на 1)
    path('battles/', views.battle_list, name='battle_list'),
    path('battles/create/', views.battle_create, name='battle_create'),
    path('battles/<int:battle_id>/join/', views.battle_join, name='battle_join'),
    path('battles/<int:battle_id>/', views.battle_arena, name='battle_arena'),
    path('api/battles/<int:battle_id>/submit/', views.api_battle_submit, name='api_battle_submit'),
    path('api/battles/<int:battle_id>/status/', views.api_battle_status, name='api_battle_status'),

    # AI & Runner API endpoints
    path('api/ai/generate-task/', views.api_generate_task, name='api_generate_task'),
    path('api/ai/<slug:slug>/hint/', views.api_code_hint, name='api_code_hint'),
    path('api/ai/<slug:slug>/review/', views.api_code_review, name='api_code_review'),
    path('api/ai/<slug:slug>/chat/', views.api_ai_chat, name='api_ai_chat'),
    path('api/tasks/<slug:slug>/custom-test/', views.api_custom_test, name='api_custom_test'),
    path('api/tasks/<slug:slug>/reveal-solution/', views.api_reveal_solution, name='api_reveal_solution'),

    # Страница конкретной задачи
    path('task/<slug:slug>/', views.task_detail, name='task_detail'),
]