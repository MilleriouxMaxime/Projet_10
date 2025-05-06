from django.contrib import admin
from .models import Project, Contributor

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'created_at')
    search_fields = ('user__username', 'project__name')
    list_filter = ('role', 'created_at')
