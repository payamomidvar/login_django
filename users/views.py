import secrets
import string
import requests

from django.core.mail import EmailMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import TokenObtainPairSerializer, UserSerializer
from env.settings import *


class RegisterView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        repeat_password = request.data['repeatPassword']
        email = request.data['email']
        if not password and not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if password != repeat_password:
            return Response({'detail': 'password and repeat password are not the same thing!'})

        try:
            User.objects.get(email=email)
            return Response({'detail': 'User already registered!'},
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            User.objects.create_user(email=email, password=password, username=username)

        return Response(status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if not password and not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=request.data['email'])
            if check_password(password, user.password):
                token = requests.post(f'http://{ip_address}:8000/users/token/', params=request.POST,
                                      data={'email': email, 'password': password})
                json_result = token.json()
                return Response({'access': json_result['access']}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'password is wrong'},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User was not registered!'},
                            status=status.HTTP_400_BAD_REQUEST)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


def get_id_by_token(request):
    access_token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    token = AccessToken(access_token)
    return token.payload['user_id']


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = get_id_by_token(request)
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        old_password = request.data['currentPassword']
        new_password = request.data['newPassword']
        repeat_new_password = request.data['repeatNewPassword']

        user_id = get_id_by_token(request)
        user = User.objects.get(id=user_id)
        if not check_password(old_password, user.password):
            return Response({'detail': 'password is wrong'})
        if new_password != repeat_new_password:
            return Response({'detail': 'New password and repeating new password are not the same thing!'})

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'password is changed'}, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        if not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User is not exist!'},
                            status=status.HTTP_400_BAD_REQUEST)
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        alphabet = letters + digits + special_chars
        password = ''
        for i in range(8):
            password += ''.join(secrets.choice(alphabet))
        user.set_password(password)
        user.save()
        EmailMessage(
            "Subject here",
            f'New password! This is {password}',
            "xacehe3014@tipent.com",
            (email,)
        )

        return Response({"message": "new password is sent"}, status=status.HTTP_201_CREATED)
