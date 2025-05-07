from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

# Nested routers for project-related resources
project_router = DefaultRouter()
project_router.register(r'contributors', ContributorViewSet, basename='contributor')
project_router.register(r'issues', IssueViewSet, basename='issue')

# Nested router for issue comments
issue_router = DefaultRouter()
issue_router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_pk>/', include(project_router.urls)),
    path('projects/<int:project_pk>/issues/<int:issue_pk>/', include(issue_router.urls)),
] 