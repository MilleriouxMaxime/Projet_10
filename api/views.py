from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor, Issue, Comment
from .permissions import (
    IsProjectContributor, IsProjectOwner, IsIssueCreatorOrProjectOwner,
    IsCommentCreatorOrProjectOwner, IsContributorManager
)
from .serializers import (
    ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
)

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsContributorManager]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        serializer.save(project=project)

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssueCreatorOrProjectOwner]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

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

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

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
