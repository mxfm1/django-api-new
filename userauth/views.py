from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView, ListAPIView
from django.contrib.auth.models import User
from rest_framework import permissions
from .serializers import (
    RegisterSerializer,
    UserSerializer,
)

from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = RegisterSerializer

class LogoutView(APIView):
    def post(self,request):
        try:
            self.permission_classes = [IsAuthenticated]
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"Cierre de sesión exitoso"}, status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response({"error":"Sesión inválida o ya expirada"}, status=status.HTTP_400_BAD_REQUEST)

class ListUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        self.permission_classes= [permissions.IsAdminUser]
        return super().get_permissions()
    # def get_queryset(self):
    #     user = self.request.user

    #     if user.is_staff:
    #         return User.objects.all()
    #     return User.objects.get(id= user.id)
        
class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated,IsAdminUser]
    lookup_field="id"
    
    def get_object(self):
        try:
            return User.objects.get(id=self.kwargs["id"])
        except User.DoesNotExist:
            raise Http404("No existe este usuario")
        
    def destroy(self,request,*args,**kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message":"Usuario eliminado con éxito"
        },status= status.HTTP_202_ACCEPTED)



    