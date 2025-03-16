from django.urls import path, include
from accounts import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('verify_email/<str:verification_code>/', views.EmailVerificationAPIView.as_view(), name='email-verification'),
    path('resend_verification_code/', views.ResendVerificationTokenAPIView.as_view(), name='resend_verification_code'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]