from django.urls import path
from .views import *

urlpatterns = [
    path('user_login',user_login,name="user_login"),
    path('logout',logout_view, name="user_logout"),
]
