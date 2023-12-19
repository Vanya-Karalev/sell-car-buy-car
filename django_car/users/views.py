from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from cars.models import Brand, Model, Engine, Gearbox, Suspension, Car, Ad, Favorites, Image, Auction, Bid
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
import re
import requests


# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('index')
#     template_name = 'signup.html'
#
#     def form_valid(self, form):
#         username = form.cleaned_data.get('username')
#         email = form.cleaned_data.get('email')
#         first_name = form.cleaned_data.get('first_name')
#         phone = form.cleaned_data.get('phone')
#         password1 = form.cleaned_data.get('password1')
#         password2 = form.cleaned_data.get('password2')
#         print(password1)
#         print(password2)
#         error_username = ''
#         error_email = ''
#         error_first_name = ''
#         error_phone = ''
#         error_password = ''
#         if (email == '' or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
#         or not re.match(r'^[a-zA-Z0-9]$', username) or first_name == '' or not first_name.isalpha() or phone == ''
#         or not re.compile(r'^\+375(25|29|33|44)\d{7}$').match(phone) or password1 != password2
#         or CustomUser.objects.filter(username=username).exists()):
#             if CustomUser.objects.filter(username=username).exists():
#                 error_username = 'Такой пользователь уже существует'
#             if not re.match(r'^[a-zA-Z0-9]$', username):
#                 error_username = 'Укажите верный username'
#             if email == '' or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
#                 error_email = 'Укажите верную почту'
#             if first_name == '' or not first_name.isalpha():
#                 error_first_name = 'Укажите верное имя'
#             if phone == '' or not re.compile(r'^\+375(25|29|33|44)\d{7}$').match(phone):
#                 error_phone = 'Укажите верный номер телефона'
#             if password1 != password2:
#                 error_password = 'Пароли не совпадают'
#             values = {'email': email,
#                       'first_name': first_name,
#                       'username': username,
#                       'phone': phone,
#                       'error_email': error_email,
#                       'error_first_name': error_first_name,
#                       'error_phone': error_phone,
#                       'error_username': error_username,
#                       'error_password': error_password,
#                       }
#             return render(self.request, 'signup.html', values)
#         else:
#             user = form.save()
#             login(self.request, self.object)
#         return super().form_valid(form)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        phone = form.cleaned_data.get('phone')
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        error_username = ''
        error_email = ''
        error_first_name = ''
        error_phone = ''
        error_password = ''
        if (email == '' or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        or not re.match(r'^[a-zA-Z0-9]+$', username) or first_name == '' or not first_name.isalpha() or phone == ''
        or not re.compile(r'^\+375(25|29|33|44)\d{7}$').match(phone) or password1 != password2
        or CustomUser.objects.filter(username=username).exists()):
            if CustomUser.objects.filter(username=username).exists():
                error_username = 'Такой пользователь уже существует'
            if not re.match(r'^[a-zA-Z0-9]+$', username):
                error_username = 'Укажите верный username'
            if email == '' or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                error_email = 'Укажите верную почту'
            if first_name == '' or not first_name.isalpha():
                error_first_name = 'Укажите верное имя'
            if phone == '' or not re.compile(r'^\+375(25|29|33|44)\d{7}$').match(phone):
                error_phone = 'Укажите верный номер телефона'
            if password1 != password2:
                error_password = 'Пароли не совпадают'
            values = {'email': email,
                      'first_name': first_name,
                      'username': username,
                      'phone': phone,
                      'error_email': error_email,
                      'error_first_name': error_first_name,
                      'error_phone': error_phone,
                      'error_username': error_username,
                      'error_password': error_password,
                      }
            return render(self.request, 'signup.html', values)
        else:
            api_url = 'http://127.0.0.1:8000/api/signup'
            data = {'username': username, 'email': email, 'first_name': first_name, 'phone': phone}
            response = requests.post(api_url, data=data)
            if response.status_code == 201:
                token = response.json().get('token')
                # Сохранение токена в сессии Django
                self.request.session['token'] = token

                return redirect('index')

            # Обработка ошибок при сохранении через API
            values = {'error_api': 'Failed to create user via API'}
            return render(self.request, 'signup.html', values)


class ProfileView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('index')
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        phone = form.cleaned_data.get('phone')
        error_email = ''
        error_first_name = ''
        error_last_name = ''
        error_phone = ''
        if (email == '' or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        or first_name == '' or not first_name.isalpha() or not last_name.isalpha() or phone == ''
        or not re.compile(r'^\+375(25|29|33|44)\d{7}$').match(phone)):
            if email == '' or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                error_email = 'Укажите верную почту'
            if first_name == '' or not first_name.isalpha():
                error_first_name = 'Укажите верное имя'
            if not last_name.isalpha():
                error_last_name = 'Укажите верную фамилию'
            if phone == '' or not re.compile(r'^\+375(25|29|33|44)\d{7}$').match(phone):
                error_phone = 'Укажите верный номер телефона'
            values = {'email': email,
                      'first_name': first_name,
                      'last_name': last_name,
                      'phone': phone,
                      'error_email': error_email,
                      'error_first_name': error_first_name,
                      'error_last_name': error_last_name,
                      'error_phone': error_phone}
            return render(self.request, 'profile.html', values)
        else:
            user = form.save()
        return super().form_valid(form)


# def LoginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#
#     context = {}
#     return render(request, 'signin.html', context)


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        api_url = 'http://127.0.0.1:8000/api/login'
        data = {'username': username, 'password': password}
        response = requests.post(api_url, data=data)

        if response.status_code == 200:
            token = response.json().get('token')

            # Сохранение токена в сессии Django
            request.session['token'] = token

            return redirect('index')

    return render(request, 'signin.html')


# def LogoutPage(request):
#     logout(request)
#     return redirect('index')


def LogoutPage(request):
    token = request.session.get('token', None)
    response = None
    if token:
        api_url = 'http://127.0.0.1:8000/api/logout'
        headers = {'Authorization': f'Token {token}'}

        response = requests.post(api_url, headers=headers)

        if response.status_code == 200:
            # Очистка токена из сессии Django
            request.session.pop('token', None)
            return redirect('index')

    return HttpResponse(status=response.status_code if response else 500)


def create_ad(request):
    brands = Brand.objects.all()
    models = Model.objects.all()
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

        error_capacity = ''
        error_fuelconsuption = ''
        error_clearance = ''
        try:
            if capacity == '' or float(capacity) < 0.1 or float(capacity) > 10:
                error_capacity = 'Укажите верный объем двигателя'
        except:
            error_capacity = 'Укажите объем двигателя в цифрах'

        try:
            if fuelconsuption == '' or float(fuelconsuption) < 1 or float(fuelconsuption) > 30:
                error_fuelconsuption = 'Укажите верный расход топлива'
        except:
            error_fuelconsuption = 'Укажите расход топлива в цифрах'

        try:
            if clearance == '' or float(clearance) < 5 or float(clearance) > 50:
                error_clearance = 'Укажите верный клиренс'
        except:
            error_clearance = 'Укажите клиренс в цифрах'

        if ((brand_name == '' or model_name == '' or not Model.objects.filter(name=model_name).exists() or mileage == ''
            or int(mileage) < 1 or int(mileage) > 1500000 or vin == '' or len(vin) != 17 or horsepower == ''
            or int(horsepower) < 1 or int(horsepower) > 2000) or torque == '' or int(torque) < 1 or int(torque) > 2000
            or year == '' or int(year) < 1900 or int(year) > 2024 or gearnumber == '' or int(gearnumber) < 1
            or int(gearnumber) > 10 or price == '' or int(price) < 1):
            error_brand_name = ''
            error_model_name = ''
            error_mileage = ''
            error_vin = ''
            error_horsepower = ''
            error_torque = ''
            error_year = ''
            error_gearnumber = ''
            error_price = ''
            if brand_name == '' or model_name == '' or not Model.objects.filter(name=model_name).exists():
                error_brand_name = 'Выберите бренд автомобиля'
                model_name = ''
                error_model_name = 'Выберите модель автомобиля'
                brand_name = ''
            if mileage == '' or int(mileage) < 1 or int(mileage) > 1500000:
                error_mileage = 'Укажите верный пробег'
            if vin == '' or len(vin) != 17:
                error_vin = 'Укажите верный vin номер (17 цифр)'
            if horsepower == '' or int(horsepower) < 1 or int(horsepower) > 1200000:
                error_horsepower = 'Укажите верные лошадиные силы'
            if torque == '' or int(torque) < 1 or int(torque) > 2000:
                error_torque = 'Укажите верный крутящий момент'
            if year == '' or int(year) < 1900 or int(year) > 2024:
                error_year = 'Укажите верный год выпуска автомобиля'
            if gearnumber == '' or int(gearnumber) < 1 or int(gearnumber) > 10:
                error_gearnumber = 'Укажите верное кол-во передач'
            if price == '' or int(price) < 1:
                error_price = 'Укажите верную стоимость автомобиля'
            values = {'brands': brands,
                      'models': models,
                      'brand_name': brand_name,
                      'model_name': model_name,
                      'mileage': mileage,
                      'vin': vin,
                      'capacity': capacity,
                      'horsepower': horsepower,
                      'torque': torque,
                      'year': year,
                      'price': price,
                      'description': description,
                      'clearance': clearance,
                      'gearnumber': gearnumber,
                      'fuelconsuption': fuelconsuption,
                      'error_brand_name': error_brand_name,
                      'error_model_name': error_model_name,
                      'error_mileage': error_mileage,
                      'error_vin': error_vin,
                      'error_horsepower': error_horsepower,
                      'error_capacity': error_capacity,
                      'error_torque': error_torque,
                      'error_fuelconsuption': error_fuelconsuption,
                      'error_year': error_year,
                      'error_clearance': error_clearance,
                      'error_gearnumber': error_gearnumber,
                      'error_price': error_price,
                      }
            return render(request, 'createad.html', values)
        else:
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
        images = request.FILES.getlist('images')
        status = request.POST.get('status')
        if price == '' or int(price) < 1:
            error_price = 'Укажите верную стоимость автомобиля'
            values = {'ad': ad,
                      'price': price,
                      'description': description,
                      'status': status,
                      'error_price': error_price}
            return render(request, 'editmyad.html', values)
        else:
            ad.price = price
            ad.description = description
            if any(images):
                ad.images.clear()
                for image in images:
                    image_instance = Image.objects.create(image=image)
                    ad.images.add(image_instance)
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


def my_auctions(request):
    user = CustomUser.objects.get(pk=request.user.id)
    date = datetime.now()
    date_string = date.strftime("%Y-%m-%dT%H:%M")
    parsed_date = timezone.datetime.strptime(date_string, "%Y-%m-%dT%H:%M")

    auctions = Auction.objects.filter(end_date__lt=parsed_date, bid__user=user)

    context = {'auctions': auctions}
    return render(request, 'myauctions.html', context)


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
    brands = Brand.objects.all()
    models = Model.objects.all()
    date = datetime.now() + timedelta(hours=3)
    date_string = date.strftime("%Y-%m-%dT%H:%M")
    min_date = timezone.datetime.strptime(date_string, "%Y-%m-%dT%H:%M")
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
        end_date_string = request.POST.get('end_date')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')
        error_capacity = ''
        error_fuelconsuption = ''
        error_clearance = ''
        error_start_date = ''
        error_end_date = ''
        start_date = ''
        end_date = ''
        try:
            if capacity == '' or float(capacity) < 0.1 or float(capacity) > 10:
                error_capacity = 'Укажите верный объем двигателя'
        except:
            error_capacity = 'Укажите объем двигателя в цифрах'

        try:
            if fuelconsuption == '' or float(fuelconsuption) < 1 or float(fuelconsuption) > 30:
                error_fuelconsuption = 'Укажите верный расход топлива'
        except:
            error_fuelconsuption = 'Укажите расход топлива в цифрах'

        try:
            if clearance == '' or float(clearance) < 5 or float(clearance) > 50:
                error_clearance = 'Укажите верный клиренс'
        except:
            error_clearance = 'Укажите клиренс в цифрах'

        try:
            if start_date_string == '':
                error_start_date = 'Укажите верную дату начала аукциона'
            else:
                start_date = timezone.datetime.strptime(start_date_string, "%Y-%m-%dT%H:%M")
        except:
            error_start_date = 'Укажите верную дату начала аукциона'

        try:
            if end_date_string == '':
                error_end_date = 'Укажите верную дату конца аукциона'
            else:
                end_date = timezone.datetime.strptime(end_date_string, "%Y-%m-%dT%H:%M")
        except:
            error_end_date = 'Укажите верную дату конца аукциона'

        if ((brand_name == '' or model_name == '' or not Model.objects.filter(name=model_name).exists() or mileage == ''
             or int(mileage) < 1 or int(mileage) > 1500000 or vin == '' or len(vin) != 17 or horsepower == ''
             or int(horsepower) < 1 or int(horsepower) > 2000) or torque == '' or int(torque) < 1 or int(torque) > 2000
                or year == '' or int(year) < 1900 or int(year) > 2024 or gearnumber == '' or int(gearnumber) < 1
                or int(gearnumber) > 10 or start_price == '' or int(start_price) < 1 or end_date <= start_date):
            error_brand_name = ''
            error_model_name = ''
            error_mileage = ''
            error_vin = ''
            error_horsepower = ''
            error_torque = ''
            error_year = ''
            error_gearnumber = ''
            error_start_price = ''

            if brand_name == '' or model_name == '' or not Model.objects.filter(name=model_name).exists():
                error_brand_name = 'Выберите бренд автомобиля'
                model_name = ''
                error_model_name = 'Выберите модель автомобиля'
                brand_name = ''
            if mileage == '' or int(mileage) < 1 or int(mileage) > 1500000:
                error_mileage = 'Укажите верный пробег'
            if vin == '' or len(vin) != 17:
                error_vin = 'Укажите верный vin номер (17 цифр)'
            if horsepower == '' or int(horsepower) < 1 or int(horsepower) > 1200000:
                error_horsepower = 'Укажите верные лошадиные силы'
            if torque == '' or int(torque) < 1 or int(torque) > 2000:
                error_torque = 'Укажите верный крутящий момент'
            if year == '' or int(year) < 1900 or int(year) > 2024:
                error_year = 'Укажите верный год выпуска автомобиля'
            if gearnumber == '' or int(gearnumber) < 1 or int(gearnumber) > 10:
                error_gearnumber = 'Укажите верное кол-во передач'
            if start_price == '' or int(start_price) < 1:
                error_start_price = 'Укажите верную стоимость автомобиля'
            if end_date <= start_date:
                error_end_date = 'Укажите верную дату конца аукциона'

            values = {'brands': brands,
                      'models': models,
                      'min_date': min_date,
                      'brand_name': brand_name,
                      'model_name': model_name,
                      'mileage': mileage,
                      'vin': vin,
                      'capacity': capacity,
                      'horsepower': horsepower,
                      'torque': torque,
                      'year': year,
                      'start_price': start_price,
                      'description': description,
                      'clearance': clearance,
                      'gearnumber': gearnumber,
                      'fuelconsuption': fuelconsuption,
                      'start_date': start_date,
                      'end_date': end_date,
                      'error_brand_name': error_brand_name,
                      'error_model_name': error_model_name,
                      'error_mileage': error_mileage,
                      'error_vin': error_vin,
                      'error_horsepower': error_horsepower,
                      'error_capacity': error_capacity,
                      'error_torque': error_torque,
                      'error_fuelconsuption': error_fuelconsuption,
                      'error_year': error_year,
                      'error_clearance': error_clearance,
                      'error_gearnumber': error_gearnumber,
                      'error_start_price': error_start_price,
                      'error_start_date': error_start_date,
                      'error_end_date': error_end_date,
                      }
            return render(request, 'createauction.html', values)
        else:
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

    context = {'brands': brands,
               'models': models,
               'min_date': min_date}
    return render(request, 'createauction.html', context)
