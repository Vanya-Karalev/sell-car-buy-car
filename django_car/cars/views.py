from django.shortcuts import render, get_object_or_404, redirect
from cars.models import Brand, Model, Engine, Gearbox, Suspension, Car, Ad


def get_cars(request):
    return render(request, 'index.html')


def buy_cars(request):
    ads = Ad.objects.all()
    context = {'ads': ads}
    return render(request, 'buy.html', context)


def car_info(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    context = {'ad': ad}
    return render(request, 'car.html', context)


def about_us(request):
    return render(request, 'aboutus.html')
