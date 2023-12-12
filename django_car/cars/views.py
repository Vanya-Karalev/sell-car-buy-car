from django.shortcuts import render, get_object_or_404, redirect
from cars.models import Brand, Model, Engine, Gearbox, Suspension, Car, Ad, Favorites
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


def car_info(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    context = {'ad': ad}
    return render(request, 'car.html', context)


def about_us(request):
    return render(request, 'aboutus.html')
