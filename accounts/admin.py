from django.contrib import admin
from .models import Profile, Classroom

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'code', 'created_at')
    search_fields = ('name', 'code', 'teacher__username')