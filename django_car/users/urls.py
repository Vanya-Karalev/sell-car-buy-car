from django.urls import path
from users.views import SignUpView, ProfileView
from . import views


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('createad/', views.create_ad, name='createad'),
    path('myads/', views.my_ads, name='myads'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', views.LoginPage, name='signin'),
    path('logout/', views.LogoutPage, name='logout'),
]
