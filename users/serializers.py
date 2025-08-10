from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['uuid', 'username', 'email', 'tech_background', 'bio', 'profile_pic']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['uuid', 'username', 'first_name', 'last_name', 'tech_stack', 'location', 'bio', 'profile_picture']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['tech_stack', 'location', 'bio', 'profile_picture', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'email': {'required': False},
            'profile_picture': {'required': False},
        }

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'uuid',
            'username',
            'first_name',
            'last_name',
            'tech_stack',
            'location',
            'bio',
            'profile_picture'
        ]