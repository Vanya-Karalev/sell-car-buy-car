from django.urls import path
from users.views import SignUpView, ProfileView
from . import views


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('createad/', views.create_ad, name='createad'),
    path('myads/', views.my_ads, name='myads'),
    path('myfavoriteads/', views.my_favorite_ads, name='myfavoriteads'),
    path('myfavoriteads/<int:ad_id>', views.favorite_ads, name='favoriteads'),
    path('myads/<int:ad_id>/', views.delete_my_ad, name='delete_ad'),
    path('myads/<int:ad_id>/edit/', views.edit_my_ad, name='edit_ad'),
    path('myads/<int:ad_id>/update/', views.update_my_ad, name='update_ad'),
    path('buycar/<int:ad_id>', views.favorite, name='favorite'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', views.LoginPage, name='signin'),
    path('logout/', views.LogoutPage, name='logout'),
]
