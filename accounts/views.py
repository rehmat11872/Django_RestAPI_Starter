import random
import string
from rest_framework.response import Response
from rest_framework import status, serializers, permissions, throttling
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import update_session_auth_hash
from accounts.models import User, Token
from .utils import send_email_verification_code 
from accounts.serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    ResendVerificationSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, extend_schema_view
from .throttles import UserLoginRateThrottle
from .schema import (
    LOGIN_RESPONSE_SCHEMA,
    USER_CREATE_RESPONSE_SCHEMA,
    PROFILE_DETAIL_SCHEMA,
    PROFILE_PATCH_SCHEMA,
    PROFILE_PUT_SCHEMA,
    EMAIL_VERIFICATION_RESPONSE_SCHEMA,
    CHANGE_PASSWORD_RESPONSE_SCHEMA,
    RESEND_VERIFICATION_RESPONSE_SCHEMA,
)

# --- User Registration ---
@extend_schema(
    request=UserSerializer,
    responses=USER_CREATE_RESPONSE_SCHEMA
)
class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    throttle_classes = [throttling.UserRateThrottle]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Please check your email to verify your account.'}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# --- Email Verification ---
class EmailVerificationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = [UserLoginRateThrottle]

    @extend_schema(responses=EMAIL_VERIFICATION_RESPONSE_SCHEMA)
    def get(self, request, verification_code):
        try:
            user = User.objects.get(email_verification_code=verification_code, is_active=False)
        except User.DoesNotExist:
            return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        # token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Email verified successfully', }, status=status.HTTP_200_OK)


# --- Email  ResendVerification  Token---
@extend_schema(
    request=ResendVerificationSerializer,
    responses=RESEND_VERIFICATION_RESPONSE_SCHEMA
)
class ResendVerificationTokenAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = [UserLoginRateThrottle]

    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email, is_active=False)
        except User.DoesNotExist:
            return Response(
                {'message': 'Invalid email or account already activated.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate a new verification code
        new_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        user.email_verification_code = new_code
        user.save()

        # Send the verification email (ensure your utility function is implemented)
        send_email_verification_code(user.email, new_code)

        return Response(
            {'message': 'Verification email resent successfully.'},
            status=status.HTTP_200_OK
        )

# --- Token Obtain Pair (Login) ---
@extend_schema(responses=LOGIN_RESPONSE_SCHEMA)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    throttle_classes = [UserLoginRateThrottle]
    permission_classes = (permissions.AllowAny,)


# --- User Profile ---
@extend_schema_view(
    get=extend_schema(responses=PROFILE_DETAIL_SCHEMA),
    patch=extend_schema(responses=PROFILE_PATCH_SCHEMA),
    put=extend_schema(responses=PROFILE_PUT_SCHEMA),
)
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    throttle_classes = [throttling.UserRateThrottle]

    def get_object(self):
        return self.request.user


# --- Change Password ---
@extend_schema(
    request=ChangePasswordSerializer,
    responses=CHANGE_PASSWORD_RESPONSE_SCHEMA
)
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data.get('old_password')):
                user.set_password(serializer.validated_data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
