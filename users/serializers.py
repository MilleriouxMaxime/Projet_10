from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'birth_date', 'first_name', 'last_name', 
                 'can_be_contacted', 'can_data_be_shared')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            birth_date=validated_data['birth_date'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            can_be_contacted=validated_data.get('can_be_contacted', False),
            can_data_be_shared=validated_data.get('can_data_be_shared', False)
        )
        return user 