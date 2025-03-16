from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from drf_spectacular.utils import OpenApiExample, inline_serializer
from rest_framework import serializers
from .serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    UserProfileSerializer,
)


ErrorResponseSerializer = inline_serializer(
    name="ErrorResponse",
    fields={
        "detail": serializers.CharField(read_only=True),
        "code": serializers.CharField(read_only=True, required=False),
    },
)

UNAUTHORIZED_EXAMPLES = [
    OpenApiExample(
        "Unauthorized",
        value={"detail": "Authentication credentials were not provided."},
        status_codes=["401"],
    ),
    OpenApiExample(
        "Invalid token",
        value={"detail": "Invalid token."},
        status_codes=["401"],
    ),
    OpenApiExample(
        "Invalid token header",
        value={"detail": "Invalid token header. No credentials provided."},
        status_codes=["401"],
    ),
]

LOGIN_RESPONSE_SCHEMA = {
    200: OpenApiResponse(
        response=MyTokenObtainPairSerializer,
        description="Successfully authenticated",
    ),
    400: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Invalid credentials",
        examples=[
            OpenApiExample(
                "Invalid Credentials",
                value={"detail": "Unable to log in with provided credentials."},
                status_codes=["400"],
            ),
            OpenApiExample(
                "Missing Fields",
                value={
                    "email": ["This field is required."],
                    "password": ["This field is required."],
                },
                status_codes=["400"],
            ),
        ],
    ),
}

USER_CREATE_RESPONSE_SCHEMA = {
    201: OpenApiResponse(
        response=UserSerializer,
        description="User successfully created",
    ),
    400: OpenApiResponse(
        description="Validation error",
        response=inline_serializer(
            name="UserCreationError",
            fields={"error": serializers.CharField()}
        ),
        examples=[
            OpenApiExample(
                "Invalid Data",
                value={"email": ["This email is already registered."], "password": ["Passwords do not match."]},
                status_codes=["400"],
            ),
        ],
    ),
}

PROFILE_DETAIL_SCHEMA = {
    200: OpenApiResponse(
        response=UserProfileSerializer,
        description="User profile data",
    ),
    401: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Authentication required",
        examples=UNAUTHORIZED_EXAMPLES,
    ),
}

PROFILE_PUT_SCHEMA = {
    200: OpenApiResponse(
        response=UserProfileSerializer,
        description="User profile updated",
    ),
    400: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Validation error",
        examples=[
            OpenApiExample(
                "Invalid Data",
                value={"password": ["Password must be at least 5 characters long."]},
                status_codes=["400"],
            ),
            OpenApiExample(
                "Missing Fields",
                value={"password": ["This field is required."]},
                status_codes=["400"],
            ),
        ],
    ),
    401: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Authentication required",
        examples=UNAUTHORIZED_EXAMPLES,
    ),
}

PROFILE_PATCH_SCHEMA = {
    200: OpenApiResponse(
        response=UserProfileSerializer,
        description="User profile updated",
    ),
    401: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Authentication required",
        examples=UNAUTHORIZED_EXAMPLES,
    ),
}


# Schema for EmailVerificationAPIView
EMAIL_VERIFICATION_RESPONSE_SCHEMA = {
    200: OpenApiResponse(
        description="Email verified successfully",
        examples=[
            OpenApiExample(
                "Success",
                value={
                    "message": "Email verified successfully",
                    "token": "your_generated_token"
                },
            )
        ],
    ),
    400: OpenApiResponse(
        description="Invalid verification code",
        examples=[
            OpenApiExample(
                "Invalid Code",
                value={"message": "Invalid verification code"},
            )
        ],
    ),
}

# Schema for ChangePasswordView
CHANGE_PASSWORD_RESPONSE_SCHEMA = {
    200: OpenApiResponse(
        description="Password changed successfully",
        examples=[
            OpenApiExample(
                "Password Changed",
                value={"message": "Password changed successfully."},
            )
        ],
    ),
    400: OpenApiResponse(
        description="Incorrect old password or validation error",
        examples=[
            OpenApiExample(
                "Incorrect Old Password",
                value={"error": "Incorrect old password."},
                status_codes=["400"],
            )
        ],
    ),
}


# Schema for RESEND_VERIFICATION_RESPONSE_SCHEMA
RESEND_VERIFICATION_RESPONSE_SCHEMA = {
    200: OpenApiResponse(
        description="Verification email resent successfully.",
        examples=[
            OpenApiExample(
                "Success",
                value={"message": "Verification email resent successfully."},
            )
        ],
    ),
    400: OpenApiResponse(
        description="Invalid email or account already activated.",
        examples=[
            OpenApiExample(
                "Invalid Request",
                value={"message": "Invalid email or account already activated."},
                status_codes=["400"],
            )
        ],
    ),
}


