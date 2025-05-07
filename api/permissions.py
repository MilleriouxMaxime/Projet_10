from rest_framework import permissions

class IsProjectContributor(permissions.BasePermission):
    """
    Custom permission to only allow project contributors to access project resources.
    """
    def has_permission(self, request, view):
        # Allow read-only access to authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # For write operations, check if user is a contributor
        project_id = view.kwargs.get('project_pk')
        if project_id:
            return request.user.contributions.filter(project_id=project_id).exists()
        return False

class IsProjectOwner(permissions.BasePermission):
    """
    Custom permission to only allow project owners to modify project details.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        project_id = view.kwargs.get('project_pk')
        if project_id:
            return request.user.created_projects.filter(id=project_id).exists()
        return False

class IsIssueCreatorOrProjectOwner(permissions.BasePermission):
    """
    Custom permission to only allow issue creators or project owners to modify issues.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return (obj.created_by.user == request.user or 
                obj.project.created_by == request.user)

class IsCommentCreatorOrProjectOwner(permissions.BasePermission):
    """
    Custom permission to only allow comment creators or project owners to modify comments.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return (obj.created_by.user == request.user or 
                obj.issue.project.created_by == request.user)

class IsContributorManager(permissions.BasePermission):
    """
    Custom permission to only allow project owners to manage contributors.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        project_id = view.kwargs.get('project_pk')
        if project_id:
            return request.user.created_projects.filter(id=project_id).exists()
        return False 