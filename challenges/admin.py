from django.contrib import admin
from .models import Task, TestCase, Submission


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'created_at')
    list_filter = ('difficulty',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TestCaseInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'status', 'created_at')
    list_filter = ('status', 'created_at')