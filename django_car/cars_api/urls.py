from django.urls import path, include
from .views import (login_user, logout_user, signup_user, update_profile, ads_status, all_ads, all_auctions,
                    get_favorite_ads, get_ad_by_id, get_auction_by_id, create_ad, update_ad, create_auction, delete_ad,
                    toggle_favorite, place_bid, get_favorite_id, get_models, get_brands)

urlpatterns = [
    path('login', login_user, name='login_user'),
    path('logout', logout_user, name='logout_user'),
    path('signup', signup_user, name='signup_user'),
    path('update', update_profile, name='update_user'),
    path('ads-status', ads_status, name='ads-status'),
    path('all-ads', all_ads, name='all-ads'),
    path('all-auctions', all_auctions, name='all-auctions'),
    path('get-favorite', get_favorite_ads, name='get-favorite'),
    path('get-favorite-ids', get_favorite_id, name='get-favorite-ids'),
    path('toggle-favorite/<ad_id>/', toggle_favorite, name='toggle-favorite'),
    path('get-ad/<ad_id>/', get_ad_by_id, name='get-ad'),
    path('get-auction/<auction_id>/', get_auction_by_id, name='get-auction'),
    path('place-bid/<auction_id>/', place_bid, name='place-bid'),
    path('create-ad', create_ad, name='create-ad'),
    path('delete-ad/<ad_id>/', delete_ad, name='delete-ad'),
    path('create-auction', create_auction, name='create-auction'),
    path('update-ad/<ad_id>/', update_ad, name='update-ad'),
    path('get-model/<brand_id>/', get_models, name='get-model'),
    path('get-brands', get_brands, name='get-brands'),
]
