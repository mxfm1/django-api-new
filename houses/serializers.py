from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Residence,ResidentProfile
from django.contrib.auth.models import User
from rest_framework import serializers

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
    owner = SimpleUserSerializer(read_only=True)  # ← mostrar owner, pero no pedirlo
    residents = ResidentProfileSerializer(many=True, read_only=True)

    resident_ids = serializers.ListField(         # ← IDs para actualizar residentes
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    new_owner_id = serializers.IntegerField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Residence
        fields = [
            "identifier",
            "owner",
            "created_by",
            "created_at",
            "updated_at",
            "residents",
            "resident_ids",
            "new_owner_id"
        ]
        read_only_fields = [
            "identifier",        # ← NO lo pedirá en el update
            "created_by",
            "created_at",
            "updated_at"
        ]

    def update(self, instance, validated_data):

        request = self.context["request"]
        print("request info",request)

        # ACTUALIZACION DE PROPIETARIO
        new_owner_id = validated_data.pop("new_owner_id",None)
        if new_owner_id is not None:
            if not request.user.is_superuser:
                raise ValidationError("Solo los administradores tienen permiso para ejecutar esta funcion")
            try:
                new_owner = User.objects.get(id=new_owner_id)
            except User.DoesNotExist:
                raise ValidationError("EL propietario no existe")
            instance.owner = new_owner
            instance.save()


        # ACTUALIZACION DE RESIDENTES
        resident_ids = validated_data.pop("resident_ids", None)

        # Actualiza campos normales
        instance = super().update(instance, validated_data)

        # Actualiza residentes
        if resident_ids is not None:
            ResidentProfile.objects.filter(
                residence=instance
            ).exclude(
                user_id__in=resident_ids
            ).update(residence=None)

            ResidentProfile.objects.filter(
                user_id__in=resident_ids
            ).update(residence=instance)

        return instance