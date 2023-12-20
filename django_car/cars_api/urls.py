from django.urls import path, include
from .views import login_user, logout_user, signup_user, ads_status, all_ads, all_auctions, get_favorite_ads

urlpatterns = [
    path('login', login_user, name='login_user'),
    path('logout', logout_user, name='logout_user'),
    path('signup', signup_user, name='signup_user'),
    path('ads-status', ads_status, name='ads-status'),
    path('all-ads', all_ads, name='all-ads'),
    path('all-auctions', all_auctions, name='all-auctions'),
    path('get-favorite', get_favorite_ads, name='get-favorite'),
]
