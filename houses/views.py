from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import Residence
from .serializers import ResidenceSerializer, UpdateResidenceSerializer,ResidenceWithUsersSerializer,UserDataSerializer
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
        user_ids = request.data.get("user_ids")

        if not user_ids or not isinstance(user_ids,list):
            return Response({
                "error":"Error al asginar usuarios a la residencia"
            },status=status.HTTP_400_BAD_REQUEST)

        # Buscar residencia
        residence = get_object_or_404(Residence, identifier=identifier)

        assigned = []
        not_Found = []

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                not_Found.append(user_id)
                continue

            profile, created = ResidentProfile.objects.get_or_create(user=user)

            profile.residence = residence
            profile.save()

            assigned.append(user_id)

        return Response({
            "message": "Residentes añadidos con éxito",
            "assigned": assigned,
            "not_found": not_Found,
            "residence": residence.identifier,
        })

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer =  UserDataSerializer(request.user)
        return Response(serializer.data)