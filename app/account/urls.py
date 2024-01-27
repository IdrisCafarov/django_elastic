from django.urls import path
from .views import *

urlpatterns = [
    path('user_login/',user_login,name="user_login"),
    path('logout/',logout_view, name="user_logout"),
    path('check_session/',check_session,name="check_session"),
    path('dashboard/',dashboard,name="dashboard"),
    path('dashboard_professors/',professors,name="dashboard_professors")
]
