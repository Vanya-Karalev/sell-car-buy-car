from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUser
from django.shortcuts import get_object_or_404


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response("missing user", status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = CustomUserSerializer(user)
        # login(request, user)
        return Response({'token': token.key, 'user': serializer.data})

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        request.auth.delete()
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def signup_user(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            # login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': serializer.data,  'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)
