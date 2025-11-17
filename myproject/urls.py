from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

# router = SimpleRouter(trailing_slash=True)  # <-- fuerza slash final
# router.register(r'users', UserDetailView, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path("api/token/",TokenObtainPairView.as_view(),name="token_obtain"),
    path("api/token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("api/auth/",include("userauth.urls")),
    path("api/houses/",include("houses.urls")),
]
