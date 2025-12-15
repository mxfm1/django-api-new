from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import InvitationSerializer
from .models import Invitation

# Create your views here.
class InvitationCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationSerializer

    def perform_create(self, serializer):
        serializer.save(
            host = self.request.user
        )

class Invitations(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationSerializer
    def get_queryset(self):
        user = self.request.user

        # obtener residencia del usuario
        try:
            residence = user.resident_profile.residence
        except:
            return Invitation.objects.none()

        if not residence:
            return Invitation.objects.none()

        return Invitation.objects.filter(
            residence=residence
        )
    
class AllInvitations(ListAPIView):
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()
    permission_classes = [IsAuthenticated]
