from django.urls import path
from .views import *

urlpatterns = [
    path("create",InvitationCreate.as_view()),
    path("user/all/",Invitations.as_view(),name="invitation-list"),
    path("user/invitations/",Invitations.as_view(),name="invitation-new-list"),
    path("all/",AllInvitations.as_view(),name="all-invitations")
]
