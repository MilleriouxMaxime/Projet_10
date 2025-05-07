from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Contributor, Issue, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'user_id', 'project', 'role', 'created_at']
        read_only_fields = ['id', 'project', 'created_at']

class IssueSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='user__username',
        read_only=True
    )
    assigned_to = serializers.SlugRelatedField(
        slug_field='user__username',
        queryset=Contributor.objects.all(),
        required=False
    )

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'project', 'created_by',
            'assigned_to', 'priority', 'status', 'tag', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'project', 'created_by', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='user__username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'issue', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'issue', 'created_by', 'created_at', 'updated_at'] 