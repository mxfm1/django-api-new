from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import Residence
from .serializers import ResidenceSerializer, UpdateResidenceSerializer,ResidenceWithUsersSerializer
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import CanManageHouses


from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Residence, ResidentProfile


class CreateResidence(CreateAPIView):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer

    permission_classes=[IsAuthenticated,CanManageHouses]

    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

class ResidenceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Residence.objects.all()
    serializer_class = ResidenceWithUsersSerializer
    permission_classes = [IsAuthenticated,CanManageHouses]
    lookup_field="identifier"
    lookup_url_kwarg = "identifier"

class ListResidence(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Residence.objects.all()
    serializer_class = ResidenceWithUsersSerializer

class AddResidentView(APIView):
    def post(self, request, identifier):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required"}, status=400)

        # Buscar residencia
        residence = get_object_or_404(Residence, identifier=identifier)

        # Buscar usuario
        user = get_object_or_404(User, id=user_id)

        # Obtener o crear perfil
        profile, created = ResidentProfile.objects.get_or_create(user=user)

        # Asignar residencia
        profile.residence = residence
        profile.save()

        return Response({
            "message": "Resident assigned successfully",
            "user_id": user.id,
            "residence": residence.identifier,
        })
