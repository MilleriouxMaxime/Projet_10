from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
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

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('created_by').all()
    permission_classes = [IsAuthenticated, IsProjectOwner]
    pagination_class = ProjectPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsContributorManager]
    pagination_class = ProjectPagination

    def get_queryset(self):
        return Contributor.objects.select_related('user').filter(
            project_id=self.kwargs['project_pk']
        )

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

    def get_queryset(self):
        return Issue.objects.select_related(
            'created_by__user', 'assigned_to__user'
        ).filter(project_id=self.kwargs['project_pk'])

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsProjectContributor()]
        return super().get_permissions()

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        contributor = Contributor.objects.get(
            user=self.request.user,
            project=project
        )
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
        return Comment.objects.select_related(
            'created_by__user'
        ).filter(issue_id=self.kwargs['issue_pk'])

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsProjectContributor()]
        return super().get_permissions()

    def perform_create(self, serializer):
        issue = Issue.objects.get(id=self.kwargs['issue_pk'])
        contributor = Contributor.objects.get(
            user=self.request.user,
            project=issue.project
        )
        serializer.save(
            issue=issue,
            created_by=contributor
        )
