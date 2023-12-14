from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from cars.models import Brand, Model, Engine, Gearbox, Suspension, Car, Ad, Favorites, Auction, Bid
from users.models import CustomUser


def get_cars(request):
    ads = Ad.objects.filter(status='True')
    favorite_ads = []

    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
        favorite_ads = Favorites.objects.filter(user=user).values_list('ad__id', flat=True)
    context = {'ads': ads,
               'favorite_ads': favorite_ads}
    return render(request, 'index.html', context)


def buy_cars(request):
    ads = Ad.objects.all()
    brand_name = ''
    start_price = ''
    end_price = ''
    if request.method == 'POST':
        brand_name = request.POST.get('selected_brand_name')
        start_price = request.POST.get('start_price')
        end_price = request.POST.get('end_price')

        filter_params = {}

        if brand_name:
            filter_params['car__brand__name'] = brand_name

        if start_price:
            filter_params['price__gte'] = start_price

        if end_price:
            filter_params['price__lte'] = end_price

        if filter_params:
            ads = Ad.objects.filter(**filter_params)

    brands = Brand.objects.all()
    favorite_ads = []

    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
        favorite_ads = Favorites.objects.filter(user=user).values_list('ad__id', flat=True)
    context = {'ads': ads,
               'brands': brands,
               'favorite_ads': favorite_ads,
               'brand_name': brand_name,
               'start_price': start_price,
               'end_price': end_price}
    return render(request, 'buy.html', context)


def auction(request):
    date = datetime.now() + timedelta(hours=3)
    date_string = date.strftime("%Y-%m-%dT%H:%M")
    parsed_date = timezone.datetime.strptime(date_string, "%Y-%m-%dT%H:%M")
    auctions = Auction.objects.filter(end_date__gt=parsed_date)
    context = {'auctions': auctions}
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
        if current_bid == '' or current_bid < 1 or current_bid < max_bid or current_bid < auction.start_price:
            error_current_bid = 'Укажите верную ставку'
            values = {'auction': auction,
                      'max_bid': max_bid,
                      'parsed_date': parsed_date,
                      'current_bid': current_bid,
                      'error_current_bid': error_current_bid}
            return render(request, 'auctioncar.html', values)
        else:
            bid = Bid.objects.create(
            user=user,
            amount=current_bid,
            date=parsed_date
            )
            auction.bid = bid
            auction.save()
            return redirect('carinfoauc', auction_id=auction_id)

    context = {'auction': auction,
               'max_bid': max_bid,
               'parsed_date': parsed_date}
    return render(request, 'auctioncar.html', context)


def about_us(request):
    return render(request, 'aboutus.html')
