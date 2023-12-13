from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from cars.models import Brand, Model, Engine, Gearbox, Suspension, Car, Ad, Favorites, Image, Auction
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('index')
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        # You can add any additional logic here if needed
        return super().form_valid(form)


def LoginPage(request):
    """Login function"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

    context = {}
    return render(request, 'signin.html', context)


def LogoutPage(request):
    """Logout function"""
    logout(request)
    return redirect('index')


def create_ad(request):
    if request.method == 'POST':
        brand_name = request.POST.get('selected_brand_name')
        model_name = request.POST.get('selected_model_name')
        mileage = request.POST.get('mileage')
        color = request.POST.get('color')
        bodytype = request.POST.get('bodytype')
        vin = request.POST.get('vin')
        enginetype = request.POST.get('enginetype')
        horsepower = request.POST.get('horsepower')
        capacity = request.POST.get('capacity')
        torque = request.POST.get('torque')
        fuelconsuption = request.POST.get('fuelconsuption')
        year = request.POST.get('year')
        suspensiontype = request.POST.get('suspensiontype')
        clearance = request.POST.get('clearance')
        gearboxtype = request.POST.get('gearboxtype')
        gearnumber = request.POST.get('gearnumber')
        price = request.POST.get('price')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')

        # Step 1: Retrieve or create related instances
        brand, created = Brand.objects.get_or_create(name=brand_name)
        model, created = Model.objects.get_or_create(name=model_name, brand=brand)
        engine, created = Engine.objects.get_or_create(type=enginetype, horse_power=horsepower, capacity=capacity,
                                                       torque=torque, fuel_consuption=fuelconsuption)
        gearbox, created = Gearbox.objects.get_or_create(type=gearboxtype, gear_number=gearnumber)
        suspension, created = Suspension.objects.get_or_create(type=suspensiontype, clearance=clearance)
        user = CustomUser.objects.get(pk=request.user.id)  # Assuming the user is logged in

        # Step 2: Create a new Car instance
        car = Car.objects.create(
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
        ad = Ad.objects.create(
            user=user,
            car=car,
            price=price,
            description=description,
        )

        for image in images:
            image_instance = Image.objects.create(image=image)
            ad.images.add(image_instance)

        return redirect('index')
    brands = Brand.objects.all()
    models = Model.objects.all()
    context = {'brands': brands,
               'models': models}
    return render(request, 'createad.html', context)


def my_ads(request):
    user = CustomUser.objects.get(pk=request.user.id)
    ads = Ad.objects.filter(user=user)
    context = {'ads': ads}
    return render(request, 'myads.html', context)


def delete_my_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    car = get_object_or_404(Car, id=ad.car.id)
    car.delete()
    return redirect('myads')


def edit_my_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    context = {'ad': ad}
    return render(request, 'editmyad.html', context)


def update_my_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        price = request.POST.get('price')
        description = request.POST.get('description')
        status = request.POST.get('status')
        ad.price = price
        ad.description = description
        ad.status = status == 'on'
        ad.save()
        return redirect('myads')
    context = {'ad': ad}
    return render(request, 'editmyad.html', context)


def my_favorite_ads(request):
    user = CustomUser.objects.get(pk=request.user.id)
    ads = Ad.objects.all()
    favorite_ads = Favorites.objects.filter(user=user)
    favoritee_ads = Favorites.objects.filter(user=user).values_list('ad__id', flat=True)
    context = {'ads': ads,
               'favorite_ads': favorite_ads,
               'favoritee_ads': favoritee_ads}
    return render(request, 'myfavoriteads.html', context)


@login_required
def favorite(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    user = request.user

    if request.method == 'POST':
        is_favorite = Favorites.objects.filter(user=user, ad=ad).exists()

        if is_favorite:
            Favorites.objects.filter(user=user, ad=ad).delete()
        else:
            Favorites.objects.create(user=user, ad=ad)

        return redirect('buycar')

    return HttpResponseForbidden("Invalid request")


@login_required
def favorite_ads(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    user = CustomUser.objects.get(pk=request.user.id)

    if request.method == 'POST':
        is_favorite = Favorites.objects.filter(user=user, ad=ad).exists()

        if is_favorite:
            Favorites.objects.filter(user=user, ad=ad).delete()
        else:
            Favorites.objects.create(user=user, ad=ad)

        return redirect('myfavoriteads')

    return HttpResponseForbidden("Invalid request")


def create_auction(request):
    if request.method == 'POST':
        brand_name = request.POST.get('selected_brand_name')
        model_name = request.POST.get('selected_model_name')
        mileage = request.POST.get('mileage')
        color = request.POST.get('color')
        bodytype = request.POST.get('bodytype')
        vin = request.POST.get('vin')
        enginetype = request.POST.get('enginetype')
        horsepower = request.POST.get('horsepower')
        capacity = request.POST.get('capacity')
        torque = request.POST.get('torque')
        fuelconsuption = request.POST.get('fuelconsuption')
        year = request.POST.get('year')
        suspensiontype = request.POST.get('suspensiontype')
        clearance = request.POST.get('clearance')
        gearboxtype = request.POST.get('gearboxtype')
        gearnumber = request.POST.get('gearnumber')
        start_price = request.POST.get('start_price')
        start_date_string = request.POST.get('start_date')
        start_date = timezone.datetime.strptime(start_date_string, "%Y-%m-%dT%H:%M")
        end_date_string = request.POST.get('end_date')
        end_date = timezone.datetime.strptime(end_date_string, "%Y-%m-%dT%H:%M")
        description = request.POST.get('description')
        images = request.FILES.getlist('images')

        # Step 1: Retrieve or create related instances
        brand, created = Brand.objects.get_or_create(name=brand_name)
        model, created = Model.objects.get_or_create(name=model_name, brand=brand)
        engine, created = Engine.objects.get_or_create(type=enginetype, horse_power=horsepower, capacity=capacity,
                                                       torque=torque, fuel_consuption=fuelconsuption)
        gearbox, created = Gearbox.objects.get_or_create(type=gearboxtype, gear_number=gearnumber)
        suspension, created = Suspension.objects.get_or_create(type=suspensiontype, clearance=clearance)
        user = CustomUser.objects.get(pk=request.user.id)  # Assuming the user is logged in

        # Step 2: Create a new Car instance
        car = Car.objects.create(
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
        auction = Auction.objects.create(
            user=user,
            car=car,
            start_price=start_price,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )

        for image in images:
            image_instance = Image.objects.create(image=image)
            auction.images.add(image_instance)

        return redirect('index')
    brands = Brand.objects.all()
    models = Model.objects.all()
    context = {'brands': brands,
               'models': models}
    return render(request, 'createauction.html', context)
