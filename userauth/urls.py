from django.urls import path
from .views import (
    RegisterView,
    UserDetailView,
    ListUsersView,
    LogoutView,
    LoginView,
)

from houses.views import MeView

from rest_framework_simplejwt.views import  (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path("register/", RegisterView.as_view(),name="register"),
    path("users/<int:id>/", UserDetailView.as_view(),name="user-view"),
    path("users/",ListUsersView.as_view(),name="list-users"),
    path("users/me",MeView.as_view(),name="my-data"),
    # path("residenceusers/",ListUsersWithResidence.as_view(),name="user-with-residence"),
    path("login/",LoginView.as_view(),name="login_view"),
    path("logout/",LogoutView.as_view(),name="logout-view"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),

]
