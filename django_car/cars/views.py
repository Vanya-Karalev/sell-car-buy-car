from datetime import datetime
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
    brands = Brand.objects.all()
    favorite_ads = []

    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
        favorite_ads = Favorites.objects.filter(user=user).values_list('ad__id', flat=True)
    # user = CustomUser.objects.get(pk=request.user.id)
    # favorite_ads = Favorites.objects.filter(user=user).values_list('ad__id', flat=True)
    context = {'ads': ads,
               'brands': brands,
               'favorite_ads': favorite_ads}
    return render(request, 'buy.html', context)


def auction(request):
    auctions = Auction.objects.all()
    bids = Bid.objects.all()
    context = {'auctions': auctions,
               'bids': bids}
    return render(request, 'auction.html', context)


def car_info(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    context = {'ad': ad}
    return render(request, 'car.html', context)


def car_info_auction(request, auction_id):
    if request.method == 'POST':
        current_bid = request.POST.get('bid')
        user = request.user
        date = datetime.now()
        date_string = date.strftime("%Y-%m-%dT%H:%M")
        parsed_date = timezone.datetime.strptime(date_string, "%Y-%m-%dT%H:%M")
        bid = Bid.objects.create(
            user=user,
            amount=current_bid,
            date=parsed_date
        )
        return redirect('carinfoauc', auction_id=auction_id)
    auction = get_object_or_404(Auction, id=auction_id)
    bids = Bid.objects.all()
    aucs = Auction.objects.all()
    print(bids)
    for bid in bids:
        print(bid.id)

    print(auction)
    if bids:
        max_bid = 0
        for bid in bids.all():
            if bid.amount > max_bid:
                max_bid = bid.amount
    else:
        max_bid = 0

    # try:
    #     bid = Auction.objects.
    #     print(bid)
    # except Bid.DoesNotExist:
    #     bid = None
    context = {'auction': auction,
               'max_bid': max_bid}
    return render(request, 'auctioncar.html', context)


def about_us(request):
    return render(request, 'aboutus.html')
