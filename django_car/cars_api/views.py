from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomUserSerializer, AdSerializer, AuctionSerializer
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUser
from cars.models import Ad, Auction, Favorites
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
        login(request, user)
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
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': serializer.data,  'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ads_status(request):
    status = request.GET.get('status', 'True')
    ads = Ad.objects.filter(status=status)
    serializer = AdSerializer(ads, many=True)
    return Response({'ads': serializer.data})


@api_view(['GET'])
def all_ads(request):
    ads = Ad.objects.all()
    serializer = AdSerializer(ads, many=True)
    return Response({'ads': serializer.data})


@api_view(['GET'])
def all_auctions(request):
    auctions = Auction.objects.all()
    serializer = AuctionSerializer(auctions, many=True)
    return Response({'auctions': serializer.data})
    # return Response({'auctions': list(auctions)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_ads(request):
    user = request.user
    favorite_ads_ids = Favorites.objects.filter(user=user).values_list('ad__id', flat=True)
    ads = Ad.objects.filter(id__in=favorite_ads_ids)

    ad_list = []
    for ad in ads:
        ad_dict = {
            'id': ad.id,
            'brand': ad.car.brand.name,
            'model': ad.car.model.name,
            'year': ad.car.year,
            'price': ad.price,
            'mileage': ad.car.mileage,
            'image_url': ad.images.first().image.url if ad.images.first() else None,
        }
        ad_list.append(ad_dict)

    return Response({'favorite_ads': ad_list})

