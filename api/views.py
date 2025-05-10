from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch, Q
from .models import Project, Contributor, Issue, Comment
from .permissions import (
    IsProjectContributor, IsProjectOwner, IsIssueCreatorOrProjectOwner,
    IsCommentCreatorOrProjectOwner, IsContributorManager
)
from .serializers import (
    ProjectSerializer, ProjectListSerializer, ContributorSerializer,
    IssueSerializer, IssueListSerializer, CommentSerializer
)
from .pagination import ProjectPagination, IssuePagination, CommentPagination
from rest_framework.exceptions import ValidationError

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectContributor]
    pagination_class = ProjectPagination

    def get_queryset(self):
        if self.action == 'list':
            # For listing, only show projects where user is a contributor
            return Project.objects.filter(
                contributors__user=self.request.user
            ).select_related('created_by').distinct()
        return Project.objects.select_related('created_by').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsProjectContributor()]

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        # Automatically create a Contributor entry for the project creator
        Contributor.objects.create(
            user=self.request.user,
            project=project,
            role='author'
        )

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsContributorManager]
    pagination_class = ProjectPagination

    def get_queryset(self):
        return Contributor.objects.select_related('user').filter(
            project_id=self.kwargs['project_pk']
        ).order_by('-created_at')  # Ensure consistent ordering

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        serializer.save(project=project)

class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsIssueCreatorOrProjectOwner]
    pagination_class = IssuePagination

    def get_serializer_class(self):
        if self.action == 'list':
            return IssueListSerializer
        return IssueSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'project_pk' in self.kwargs:
            context['project'] = Project.objects.get(id=self.kwargs['project_pk'])
        return context

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        try:
            # Check if user is a contributor to the project
            Contributor.objects.get(
                user=self.request.user,
                project=project
            )
            # If they are a contributor, show all issues for the project
            return Issue.objects.select_related(
                'created_by__user', 'assigned_to__user'
            ).filter(
                project_id=self.kwargs['project_pk']
            ).order_by('-created_at')  # Order by creation date, newest first
        except Contributor.DoesNotExist:
            return Issue.objects.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsProjectContributor()]
        return super().get_permissions()

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        # Get the most recent contributor record for this user and project
        contributor = Contributor.objects.filter(
            user=self.request.user,
            project=project
        ).order_by('-created_at').first()
        
        if not contributor:
            raise ValidationError("You must be a contributor to create issues")
            
        serializer.save(
            project=project,
            created_by=contributor,
            assigned_to=contributor
        )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentCreatorOrProjectOwner]
    pagination_class = CommentPagination

    def get_queryset(self):
        issue = Issue.objects.get(id=self.kwargs['issue_pk'])
        try:
            # Check if user is a contributor to the project
            Contributor.objects.get(
                user=self.request.user,
                project=issue.project
            )
            # If they are a contributor, show all comments for the issue
            return Comment.objects.select_related(
                'created_by__user'
            ).filter(
                issue_id=self.kwargs['issue_pk']
            ).order_by('-created_at')  # Order by creation date, newest first
        except Contributor.DoesNotExist:
            return Comment.objects.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsProjectContributor()]
        return super().get_permissions()

    def perform_create(self, serializer):
        issue = Issue.objects.get(id=self.kwargs['issue_pk'])
        # Get the most recent contributor record for this user and project
        contributor = Contributor.objects.filter(
            user=self.request.user,
            project=issue.project
        ).order_by('-created_at').first()
        
        if not contributor:
            raise ValidationError("You must be a contributor to create comments")
            
        serializer.save(
            issue=issue,
            created_by=contributor
        )
