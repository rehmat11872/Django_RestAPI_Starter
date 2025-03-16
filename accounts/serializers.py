import json
import random
import string
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .utils import send_email_verification_code
from drf_spectacular.utils import extend_schema_field

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the base class to validate and get the JWT tokens
        data = super().validate(attrs)
        # Add custom fields if desired
        data['email'] = self.user.email
        data['message'] = 'Login successful'
        return data

    # If you want to include extra claims in the token itself, override get_token.
    # For example:
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email_verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.email_verification_code = email_verification_code  
        user.is_active = False  # or False if you require email verification
        user.save()
        send_email_verification_code(user.email, email_verification_code)
        return user

    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)
        user: User = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user   