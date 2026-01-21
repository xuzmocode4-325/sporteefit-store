from django.urls import path
from .views import EmailVerificationView

urlpatterns = [
    path(
        'verify-email/<uidb64>/<token>/',
        EmailVerificationView.as_view(),
        name='email-verification'
    ),
]
