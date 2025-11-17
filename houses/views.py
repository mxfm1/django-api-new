from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Residence
from .serializers import ResidenceSerializer, UpdateResidenceSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import CanManageHouses


class CreateResidence(CreateAPIView):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer

    permission_classes=[IsAuthenticated,CanManageHouses]

    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

class ResidenceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Residence.objects.all()
    serializer_class = UpdateResidenceSerializer
    permission_classes = [IsAuthenticated,CanManageHouses]
    lookup_field="identifier"
    lookup_url_kwarg = "identifier"

    

