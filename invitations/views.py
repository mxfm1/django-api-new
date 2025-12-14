from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import InvitationSerializer

# Create your views here.
class InvitationCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationSerializer

    def perform_create(self, serializer):
        serializer.save(
            host = self.request.user
        )
