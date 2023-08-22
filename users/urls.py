from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import RegisterView, LoginView, EmailTokenObtainPairView, UserView, ForgotPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('users/token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', UserView.as_view()),
    path('user/change_password/', UserView.as_view()),
    path('user/forgot_password/', ForgotPasswordView.as_view()),

]
