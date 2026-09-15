from django.contrib import admin
from .models import Task, TestCase, Submission, Tag, Assignment, CodeBattle, TaskSolutionView


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
    list_display = ('user', 'task', 'status', 'execution_time', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'task__title')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'task', 'due_date', 'created_at')
    list_filter = ('created_at', 'due_date')
    search_fields = ('classroom__name', 'task__title')


@admin.register(CodeBattle)
class CodeBattleAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'creator', 'opponent', 'winner', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('creator__username', 'opponent__username', 'task__title')


@admin.register(TaskSolutionView)
class TaskSolutionViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('user__username', 'task__title')