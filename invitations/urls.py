from django.urls import path
from .views import *

urlpatterns = [
    path("create",InvitationCreate.as_view())
]
