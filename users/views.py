from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

        return Response(status=status.HTTP_200_OK)
