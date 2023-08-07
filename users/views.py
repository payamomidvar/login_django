from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import TokenObtainPairSerializer, UserSerializer


class RegisterView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        if not password and not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            User.objects.get(email=email)
            return Response({'detail': 'User already registered!'},
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            User.objects.create_user(email=email, password=password, username=username)

        return Response(status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def get(self, request):
        email = request.data['email']
        password = request.data['password']
        if not password and not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=request.data['email'])
            if check_password(password, user.password):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'password is wrong'},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User was not registered!'},
                            status=status.HTTP_400_BAD_REQUEST)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        old_password = request.data['currentPassword']
        new_password = request.data['newPassword']
        repeat_new_password = request.data['repeatNewPassword']

        user = User.objects.get(id=pk)
        if not check_password(old_password, user.password):
            return Response({'detail': 'password is wrong'})
        if new_password != repeat_new_password:
            return Response({'detail': 'New password and repeating new password are not the same'})

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'password is changed'}, status=status.HTTP_200_OK)
