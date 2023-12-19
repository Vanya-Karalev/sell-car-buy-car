from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from users.models import CustomUser
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from .serializers import CustomUserSerializer
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        request.auth.delete()  # Удаление токена
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def signup_user(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)
