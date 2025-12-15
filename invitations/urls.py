from django.urls import path
from .views import *

urlpatterns = [
    path("create",InvitationCreate.as_view()),
    path("user/all/",Invitations.as_view(),name="invitation-list")
]
