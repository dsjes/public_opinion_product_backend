from django.urls import path
from .views import ClientSingUpView, MemberSignUpView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)

urlpatterns = [
    path("client-signup", ClientSingUpView.as_view(), name="client_signup"),
    path("member-signup", MemberSignUpView.as_view(), name="member_signup"),
    path("token/", CustomTokenObtainPairView.as_view(), name="access_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # path("plan", PlanView.as_view()),
]
