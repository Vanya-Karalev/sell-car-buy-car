from django.urls import path
from . import views

urlpatterns = [
    path('buycar/', views.buy_cars, name="buycar"),
    path('buycar/<int:ad_id>', views.car_info, name='carinfo'),
    path('aboutus/', views.about_us, name="aboutus"),
    path('', views.get_cars, name="index"),
]
