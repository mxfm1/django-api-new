from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Residence,ResidentProfile
from django.contrib.auth.models import User

class ResidenceSerializer(ModelSerializer):
    class Meta:
        fields = ["identifier","owner","created_by","created_at","updated_at"]
        model = Residence
        # read_only_fields = ["identifier", "created_by", "created_at", "updated_at"]

    def validate_owner(self,user):
        if user.is_superuser:
            raise ValidationError("Un usuario administrador no puede ser dueño de una residencia")
        return user

    def validate_identifier(self,value):
        identifier = value.upper()
        
        if Residence.objects.filter(identifier=identifier).exists():
            raise ValidationError("Ya existe una residencia registrada con ese identificador")
        
        return identifier
    

class UpdateResidenceSerializer(ModelSerializer):
    class Meta:
        model = Residence
        fields = ["identifier", "owner", "created_by", "created_at", "updated_at"]
        read_only_fields = ["identifier", "created_by", "created_at", "updated_at"]

    def validate_owner(self, user):
        if user.is_superuser:
            raise ValidationError("Un usuario administrador no puede ser dueño de una residencia")
        return user
    
class ListResidenceSerializer(ModelSerializer):
    class Meta:
        model = Residence
        fields = ["identifier", "owner", "created_by", "created_at", "updated_at"]
        read_only_fields = ["identifier", "created_by", "created_at", "updated_at"]


class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ResidentProfileSerializer(ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
     
    class Meta:
        model = ResidentProfile
        fields = []

    def to_representation(self, instance):
        return SimpleUserSerializer(instance.user).data

class ResidenceWithUsersSerializer(ModelSerializer):
    residents = ResidentProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Residence
        fields = [
            "identifier",
            "owner",
            "created_by",
            "created_at",
            "updated_at",
            "residents",
        ]