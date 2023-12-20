from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from cars.models import Brand, Model, Engine, Gearbox, Suspension, Car, Ad, Favorites, Auction, Bid, Image
from users.models import CustomUser
from django.http import JsonResponse
from django.db.models import F
from django.db.models import OuterRef, Subquery
import requests


def get_cars(request):
    # api_url = 'http://127.0.0.1:8000/api/ads'
    # data = {'status': 'True'}
    # response = requests.get(api_url, data=data)
    # ads = None
    # if response.status_code == 200:
    #     ads = response.json().get('ads')
    #     print(ads)

    ads = Ad.objects.filter(status='True')[0:1]
    total_ads = Ad.objects.count()
    favorite_ads = []

    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
        favorite_ads = Favorites.objects.filter(user=user).values_list('ad__id', flat=True)

    # api_url = 'http://127.0.0.1:8000/api/get-favorite'
    # token = request.session.get('token', None)
    # headers = {'Authorization': f'Token {token}'}
    # response = requests.get(api_url, headers=headers)
    # if response.status_code == 200:
    #     print(response.json().get('favorite_ads'))

    api_url = 'http://127.0.0.1:8000/api/get-ad/17'
    response = requests.get(api_url)
    if response.status_code == 200:
        print(response.json().get('ad'))

    context = {'ads': ads,
               'total_ads': total_ads,
               'favorite_ads': favorite_ads}
    return render(request, 'index.html', context)


def load_more(request):
    total_item = int(request.GET.get('total_item'))
    limit = 1

    subquery = Image.objects.filter(ad=OuterRef('id')).values('image').order_by('id')[:1]

    ads = Ad.objects.filter(status='True').select_related('car__brand', 'car__model').annotate(
        brand_name=F('car__brand__name'),
        model_name=F('car__model__name'),
        year=F('car__year'),
        mileage=F('car__mileage'),
        image=Subquery(subquery)
    ).values('id', 'price', 'brand_name', 'model_name', 'year', 'mileage', 'image')[total_item:total_item + limit]

    data = {'ads': list(ads)}
    return JsonResponse(data)


def buy_cars(request):
    ads = Ad.objects.all()
    brand_name = ''
    model_name = ''
    start_price = ''
    end_price = ''
    start_year = ''
    end_year = ''
    start_mileage = ''
    end_mileage = ''
    if request.method == 'POST':
        brand_name = request.POST.get('selected_brand_name')
        model_name = request.POST.get('selected_model_name')
        start_price = request.POST.get('start_price')
        end_price = request.POST.get('end_price')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        start_mileage = request.POST.get('start_mileage')
        end_mileage = request.POST.get('end_mileage')

        filter_params = {}

        if brand_name:
            filter_params['car__brand__name'] = brand_name

        if model_name:
            filter_params['car__model__name'] = model_name

        if start_price:
            filter_params['price__gte'] = start_price

        if end_price:
            filter_params['price__lte'] = end_price

        if start_year:
            filter_params['car__year__gte'] = start_year

        if end_year:
            filter_params['car__year__lte'] = end_year

        if start_mileage:
            filter_params['car__mileage__gte'] = start_mileage

        if end_mileage:
            filter_params['car__mileage__lte'] = end_mileage

        if filter_params:
            ads = Ad.objects.filter(**filter_params)

    brands = Brand.objects.all()
    models = Model.objects.all()
    favorite_ads = []

    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
        favorite_ads = Favorites.objects.filter(user=user).values_list('ad__id', flat=True)
    context = {'ads': ads,
               'brands': brands,
               'models': models,
               'favorite_ads': favorite_ads,
               'brand_name': brand_name,
               'model_name': model_name,
               'start_price': start_price,
               'end_price': end_price,
               'start_year': start_year,
               'end_year': end_year,
               'start_mileage': start_mileage,
               'end_mileage': end_mileage,
               }
    return render(request, 'buy.html', context)


def auction(request):
    date = datetime.now() + timedelta(hours=3)
    date_string = date.strftime("%Y-%m-%dT%H:%M")
    parsed_date = timezone.datetime.strptime(date_string, "%Y-%m-%dT%H:%M")
    auctions = Auction.objects.filter(end_date__gt=parsed_date)
    brand_name = ''
    model_name = ''
    start_price = ''
    end_price = ''
    start_year = ''
    end_year = ''
    start_mileage = ''
    end_mileage = ''
    if request.method == 'POST':
        brand_name = request.POST.get('selected_brand_name')
        model_name = request.POST.get('selected_model_name')
        start_price = request.POST.get('start_price')
        end_price = request.POST.get('end_price')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        start_mileage = request.POST.get('start_mileage')
        end_mileage = request.POST.get('end_mileage')

        filter_params = {}

        if brand_name:
            filter_params['car__brand__name'] = brand_name

        if model_name:
            filter_params['car__model__name'] = model_name

        if start_price:
            filter_params['price__gte'] = start_price

        if end_price:
            filter_params['price__lte'] = end_price

        if start_year:
            filter_params['car__year__gte'] = start_year

        if end_year:
            filter_params['car__year__lte'] = end_year

        if start_mileage:
            filter_params['car__mileage__gte'] = start_mileage

        if end_mileage:
            filter_params['car__mileage__lte'] = end_mileage

        if filter_params:
            auctions = Auction.objects.filter(**filter_params)

    brands = Brand.objects.all()
    models = Model.objects.all()
    context = {'auctions': auctions,
               'brands': brands,
               'models': models,
               'brand_name': brand_name,
               'model_name': model_name,
               'start_price': start_price,
               'end_price': end_price,
               'start_year': start_year,
               'end_year': end_year,
               'start_mileage': start_mileage,
               'end_mileage': end_mileage}
    return render(request, 'auction.html', context)


def car_info(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    context = {'ad': ad}
    return render(request, 'car.html', context)


def car_info_auction(request, auction_id):
    date = datetime.now() + timedelta(hours=3)
    date_string = date.strftime("%Y-%m-%dT%H:%M")
    parsed_date = timezone.datetime.strptime(date_string, "%Y-%m-%dT%H:%M")
    auction = get_object_or_404(Auction, id=auction_id)
    max_bid = 0
    if auction.bid:
        bids = Bid.objects.filter(id=auction.bid.id)
        if bids:
            for bid in bids.all():
                if bid.amount > max_bid:
                    max_bid = bid.amount
        else:
            max_bid = 0
    if request.method == 'POST':
        current_bid = request.POST.get('bid')
        user = request.user
        if current_bid == '' or int(current_bid) < 1 or int(current_bid) < int(max_bid) or int(current_bid) < int(auction.start_price):
            error_current_bid = 'Укажите верную ставку'
            values = {'auction': auction,
                      'max_bid': max_bid,
                      'parsed_date': parsed_date,
                      'current_bid': current_bid,
                      'error_current_bid': error_current_bid}
            return render(request, 'auctioncar.html', values)
        else:
            bid = Bid.objects.create(user=user, amount=current_bid, date=parsed_date)
            auction.bid = bid
            auction.save()
            return redirect('carinfoauc', auction_id=auction_id)

    context = {'auction': auction,
               'max_bid': max_bid,
               'parsed_date': parsed_date}
    return render(request, 'auctioncar.html', context)


def about_us(request):
    return render(request, 'aboutus.html')
