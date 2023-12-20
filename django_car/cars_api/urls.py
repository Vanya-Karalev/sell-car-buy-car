from django.urls import path, include
from .views import (login_user, logout_user, signup_user, ads_status, all_ads, all_auctions, get_favorite_ads,
                    get_ad_by_id)

urlpatterns = [
    path('login', login_user, name='login_user'),
    path('logout', logout_user, name='logout_user'),
    path('signup', signup_user, name='signup_user'),
    path('ads-status', ads_status, name='ads-status'),
    path('all-ads', all_ads, name='all-ads'),
    path('all-auctions', all_auctions, name='all-auctions'),
    path('get-favorite', get_favorite_ads, name='get-favorite'),
    path('get-ad/<ad_id>/', get_ad_by_id, name='get-ad'),
]
