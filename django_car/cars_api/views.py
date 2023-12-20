from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (CustomUserSerializer, AuctionSerializer, AdSerializer, BrandSerializer, ModelSerializer,
                          EngineSerializer, GearboxSerializer, SuspensionSerializer, CarSerializer, ImageSerializer,
                          FavoritesSerializer, CarsSerializer)
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUser
from cars.models import Ad, Auction, Favorites, Image, Car, Bid, Model, Brand, Gearbox, Suspension, Engine
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone


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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user

    if request.method == 'PUT':
        serializer = CustomUserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'user': serializer.data}, status=status.HTTP_200_OK)
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_ads(request):
    user = request.user
    favorite_ads = Favorites.objects.filter(user=user)
    ad_ids = favorite_ads.values_list('ad', flat=True)
    ads = Ad.objects.filter(id__in=ad_ids)
    serializer = AdSerializer(ads, many=True)
    return Response({'favorite_ads': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_id(request):
    user = request.user
    favorite_ads = Favorites.objects.filter(user=user)
    ad_ids = favorite_ads.values_list('ad', flat=True)
    return Response({'favorite_ad_ids': ad_ids})


@api_view(['GET'])
def get_ad_by_id(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    serializer = AdSerializer(ad)
    return Response({'ad': serializer.data})


@api_view(['GET'])
def get_models(request, brand_id):
    models = get_object_or_404(Model, id=brand_id)
    serializer = ModelSerializer(models)
    return Response({'models': serializer.data})


@api_view(['GET'])
def get_brands(request):
    brands = get_object_or_404(Brand)
    serializer = ModelSerializer(brands)
    return Response({'brands': serializer.data})


@api_view(['GET'])
def get_auction_by_id(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    serializer = AuctionSerializer(auction)
    return Response({'auction': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ad(request):
    try:
        data = request.data
        brand_name = data.get('brand')['selected_brand_name']
        model_name = data.get('model')['selected_model_name']

        mileage = data.get('car')['mileage']
        color = data.get('car')['color']
        bodytype = data.get('car')['body_type']
        vin = data.get('car')['vin']

        enginetype = data.get('engine')['type']
        horsepower = data.get('engine')['horse_power']
        capacity = data.get('engine')['capacity']
        torque = data.get('engine')['torque']
        fuelconsuption = data.get('engine')['fuel_consuption']

        year = data.get('car')['year']
        suspensiontype = data.get('suspension')['type']
        clearance = data.get('suspension')['clearance']

        gearboxtype = data.get('gearbox')['type']
        gearnumber = data.get('gearbox')['gear_number']

        price = data.get('price')
        description = data.get('description')

        images = data.get('blob')

        # Step 1: Retrieve or create related instances
        brand, created = Brand.objects.get_or_create(name=brand_name)
        model, created = Model.objects.get_or_create(name=model_name, brand=brand)
        engine, created = Engine.objects.get_or_create(type=enginetype, horse_power=horsepower, capacity=capacity,
                                                       torque=torque, fuel_consuption=fuelconsuption)
        gearbox, created = Gearbox.objects.get_or_create(type=gearboxtype, gear_number=gearnumber)
        suspension, created = Suspension.objects.get_or_create(type=suspensiontype, clearance=clearance)
        user = request.user

        # Step 2: Create a new Car instance
        car, created = Car.objects.get_or_create(
            brand=brand,
            model=model,
            mileage=mileage,
            body_type=bodytype,
            year=year,
            color=color,
            vin=vin,
        )
        car.engines.add(engine)
        car.gearboxes.add(gearbox)
        car.suspensions.add(suspension)

        # Step 3: Create a new Ad instance
        ad, created = Ad.objects.get_or_create(
            user=user,
            car=car,
            price=price,
            description=description,
        )

        # Step 4: Add images to the Ad instance
        for image in images:
            image_instance = Image.objects.create(blob=image['image'])
            ad.images.add(image_instance)

        return Response(AdSerializer(ad).data, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_ad(request, ad_id):
    try:
        ad = Ad.objects.get(pk=ad_id, user=request.user)
    except Ad.DoesNotExist:
        return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AdSerializer(instance=ad, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update images
            if 'images' in request.data:
                ad.images.clear()
                for image_data in request.data['images']:
                    image_instance = Image.objects.create(image=image_data)
                    ad.images.add(image_instance)

            return Response({'message': 'Ad updated successfully', 'ad': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_auction(request):
    data = request.data

    brand_serializer = BrandSerializer(data=data['brand'])
    brand_serializer.is_valid(raise_exception=True)
    brand = brand_serializer.save()

    model_serializer = ModelSerializer(data=data['model'])
    model_serializer.is_valid(raise_exception=True)
    model = model_serializer.save(brand=brand)

    engine_serializer = EngineSerializer(data=data['engine'])
    engine_serializer.is_valid(raise_exception=True)
    engine = engine_serializer.save()

    gearbox_serializer = GearboxSerializer(data=data['gearbox'])
    gearbox_serializer.is_valid(raise_exception=True)
    gearbox = gearbox_serializer.save()

    suspension_serializer = SuspensionSerializer(data=data['suspension'])
    suspension_serializer.is_valid(raise_exception=True)
    suspension = suspension_serializer.save()

    car_serializer = CarSerializer(data=data['car'])
    car_serializer.is_valid(raise_exception=True)
    car = car_serializer.save(brand=brand, model=model, engines=[engine], gearboxes=[gearbox], suspensions=[suspension])

    auction_serializer = AuctionSerializer(data=data)
    auction_serializer.is_valid(raise_exception=True)
    auction = auction_serializer.save(user=request.user, car=car)

    for image_data in data.get('images', []):
        image_serializer = ImageSerializer(data=image_data)
        image_serializer.is_valid(raise_exception=True)
        image_instance = image_serializer.save()
        auction.images.add(image_instance)

    return Response(AuctionSerializer(auction).data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    car = get_object_or_404(Car, id=ad.car.id)

    # Удаление связанных объектов
    ad.delete()
    car.delete()

    return Response({'message': 'Ad and Car deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    user = request.user
    message = None
    if request.method == 'POST':
        # Добавление в избранное
        Favorites.objects.get_or_create(user=user, ad=ad)
        message = 'Ad added to favorites'
    elif request.method == 'DELETE':
        # Удаление из избранного
        Favorites.objects.filter(user=user, ad=ad).delete()
        message = 'Ad removed from favorites'

    return Response({'message': message}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    user = request.user
    current_bid = request.data.get('amount')

    if current_bid is not None and current_bid > auction.start_price:
        # Создание новой ставки
        date = datetime.now()
        date_string = date.strftime("%Y-%m-%dT%H:%M")
        parsed_date = timezone.datetime.strptime(date_string, "%Y-%m-%dT%H:%M")
        bid = Bid.objects.create(user=user, amount=current_bid, date=parsed_date)
        auction.bid = bid
        auction.save()
        message = 'Bid placed successfully'
        return Response({'message': message}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid bid amount'}, status=status.HTTP_400_BAD_REQUEST)
