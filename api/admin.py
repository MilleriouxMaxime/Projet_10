from django.contrib import admin
from .models import Project, Contributor, Issue, Comment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('type', 'created_at')

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'created_at')
    search_fields = ('user__username', 'project__name')
    list_filter = ('role', 'created_at')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_by', 'assigned_to', 'priority', 'status', 'tag', 'created_at')
    search_fields = ('title', 'description', 'project__name')
    list_filter = ('priority', 'status', 'tag', 'created_at')
    raw_id_fields = ('project', 'created_by', 'assigned_to')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('issue', 'created_by', 'created_at', 'updated_at')
    search_fields = ('content', 'issue__title', 'created_by__user__username')
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('issue', 'created_by')
