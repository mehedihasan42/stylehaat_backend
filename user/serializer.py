from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'role',
            'password',
            'password2'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            role=validated_data['role'],
            password=validated_data['password'],
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add user info to response
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email
        }
        return data        