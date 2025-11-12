from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(['POST'])
def login(request):
    print(request.data)
    return Response({"message":"Login Exitoso"})

@api_view(['POST'])
def register(request):
    print(request.data)
    return Response({"message":"Registro exitoso"})

@api_view(['GET'])
def profile(request):
    return Response({"message":"Data del perfil enviada"})