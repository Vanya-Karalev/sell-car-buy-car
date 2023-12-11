from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from cars.models import Brand, Model, Engine, Gearbox, Suspension, Car, Ad
from users.models import CustomUser
from django.http import JsonResponse


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            return redirect('index')
        else:
            return render(request, self.template_name, {'form', form})


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

        return redirect('index')
    brands = Brand.objects.all()
    models = Model.objects.all()
    context = {'brands': brands,
               'models': models}
    return render(request, 'createad.html', context)


def my_ads(request):
    return render(request, 'myads.html')
