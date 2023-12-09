from django.urls import path
from users.views import SignUpView
from . import views


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', views.LoginPage, name='signin'),
    path('logout/', views.LogoutPage, name='logout'),
]
