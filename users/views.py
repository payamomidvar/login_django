from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password


from .models import User


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
